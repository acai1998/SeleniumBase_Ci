#!/usr/bin/env bash
# =============================================================================
# SeleniumBase CI 测试执行入口脚本
# =============================================================================
# 职责：
#   1. 标记执行开始（通知平台）
#   2. git clone 测试用例仓库
#   3. 安装仓库自身的额外依赖
#   4. 构造并执行 pytest 命令
#   5. 回调平台汇报结果（包含重试）
#
# 所有运行参数通过环境变量注入（docker run -e），无需修改本脚本。
#
# 必需变量：
#   RUN_ID        平台执行批次 ID
#   PLATFORM_URL  平台 API 地址（如 https://autotest.wiac.xyz）
#
# 可选变量：
#   REPO_URL      测试用例仓库 Git 地址（不传则使用当前 /workspace 目录）
#   REPO_BRANCH   仓库分支，默认 master
#   SCRIPT_PATHS  逗号分隔的脚本路径（如 examples/E/test_x.py,examples/A/test_y.py）
#   MARKER        pytest marker（如 smoke），与 SCRIPT_PATHS 互斥，SCRIPT_PATHS 优先
#   CALLBACK_URL       回调完整地址，默认 ${PLATFORM_URL}/api/jenkins/callback
#   PARALLEL_WORKERS   并发进程数（0/false=串行，auto=按CPU核数，N=指定N个进程）
#                      依赖 pytest-xdist；未设置时默认串行
# =============================================================================

set -eo pipefail

# ── 记录启动时间（用于计算执行时长）─────────────────────────────────────────
START_MS=$(date +%s%3N)

# ── 必需参数校验 ──────────────────────────────────────────────────────────────
if [ -z "${RUN_ID}" ]; then
    echo "❌ 必须传入环境变量 RUN_ID" >&2
    exit 1
fi
# RUN_ID 必须是纯整数，防止注入 Python/JSON 源码
if ! echo "${RUN_ID}" | grep -qE '^[0-9]+$'; then
    echo "❌ RUN_ID 格式错误（必须为纯整数，当前值: '${RUN_ID}'）" >&2
    exit 1
fi
if [ -z "${PLATFORM_URL}" ]; then
    echo "❌ 必须传入环境变量 PLATFORM_URL" >&2
    exit 1
fi

# ── 变量初始化 ────────────────────────────────────────────────────────────────
REPO_BRANCH="${REPO_BRANCH:-master}"
CALLBACK_URL="${CALLBACK_URL:-${PLATFORM_URL}/api/jenkins/callback}"
REPORT_FILE="/workspace/test-report.json"
JUNIT_FILE="/workspace/junit.xml"

echo "══════════════════════════════════════════════════════"
echo "  SeleniumBase CI Runner"
echo "  RUN_ID       : ${RUN_ID}"
echo "  PLATFORM_URL : ${PLATFORM_URL}"
echo "  REPO_URL     : ${REPO_URL:-（未指定，使用当前目录）}"
echo "  REPO_BRANCH  : ${REPO_BRANCH}"
echo "  SCRIPT_PATHS : ${SCRIPT_PATHS:-（未指定）}"
echo "  MARKER       : ${MARKER:-（未指定）}"
echo "  CALLBACK_URL      : ${CALLBACK_URL}"
echo "  PARALLEL_WORKERS  : ${PARALLEL_WORKERS:-（未设置，默认串行）}"
echo "══════════════════════════════════════════════════════"

# ── 1. 标记执行开始 ───────────────────────────────────────────────────────────
echo ""
echo "▶ [1/5] 标记执行开始..."
curl -sS -X POST "${PLATFORM_URL}/api/executions/${RUN_ID}/start" \
    -H 'Content-Type: application/json' \
    --connect-timeout 5 --max-time 10 -k \
    || echo "  ⚠ 标记开始失败（平台暂时不可达），继续执行"

# ── 2. 克隆测试用例仓库 ───────────────────────────────────────────────────────
echo ""
echo "▶ [2/5] 准备测试代码..."

REPO_DIR="/workspace/repo"

if [ "${REPO_PRELOADED}" = "true" ] && [ -d "/repo" ]; then
    # Jenkinsfile 已在宿主机完成 git clone，并通过 -v ${repoDir}:/repo 挂载进容器。
    # 直接使用已挂载的 /repo，跳过 clone，避免以 root 身份在 /workspace/repo 写入
    # 从而导致宿主机 jenkins 用户无权清理的权限问题。
    echo "  ✅ REPO_PRELOADED=true，使用宿主机已挂载的 /repo 目录（跳过 git clone）"
    REPO_DIR="/repo"
    cd "${REPO_DIR}"
elif [ -n "${REPO_URL}" ]; then
    echo "  git clone ${REPO_URL} @ ${REPO_BRANCH}"
    git clone --single-branch --branch "${REPO_BRANCH}" "${REPO_URL}" "${REPO_DIR}"
    cd "${REPO_DIR}"
else
    echo "  ⚠ 未传入 REPO_URL，使用容器内 /workspace 目录"
    cd /workspace
    REPO_DIR="/workspace"
fi

echo "  工作目录: $(pwd)"

# ── 3. 安装仓库自身的额外依赖 ─────────────────────────────────────────────────
echo ""
echo "▶ [3/5] 安装仓库依赖..."
if [ -f "requirements.txt" ]; then
    # 计算 requirements.txt 的 MD5，与镜像预装时的哈希比对
    # 若镜像内已预装相同内容（/opt/preinstalled_req.md5），则跳过安装，节省 2~5 分钟
    REQ_MD5=$(md5sum requirements.txt | cut -d' ' -f1)
    PREINSTALLED_MD5_FILE="/opt/preinstalled_req.md5"
    if [ -f "${PREINSTALLED_MD5_FILE}" ] && [ "$(cat ${PREINSTALLED_MD5_FILE})" = "${REQ_MD5}" ]; then
        echo "  ✅ requirements.txt 与镜像预装版本一致（MD5: ${REQ_MD5}），跳过 pip install"
    else
        echo "  安装 requirements.txt（MD5: ${REQ_MD5}，镜像预装版本不匹配或不存在）..."
        pip install --no-cache-dir -q \
            -i https://mirrors.aliyun.com/pypi/simple/ \
            --trusted-host mirrors.aliyun.com \
            -r requirements.txt
        echo "  ✅ 依赖安装完成"
    fi
else
    echo "  ℹ 未找到 requirements.txt，跳过"
fi

# ── 4. 构造并执行 pytest ──────────────────────────────────────────────────────
echo ""
echo "▶ [4/5] 执行测试..."

# 仓库目录结构：
#   repo/
#     examples/         ← pytest.ini 中 testpaths = examples，即实际测试文件根目录
#       A/test_xxx.py
#       E/test_xxx.py
#
# 数据库 scriptPath 格式：examples/E/test_xxx.py（相对于仓库根）
# pytest 在仓库根执行时，直接传 examples/E/test_xxx.py 即可，无需 strip 前缀
# （pytest.ini 已在仓库根，让 pytest 自动读取配置）

# ── 构造 pytest 命令（Shell 数组，安全处理含空格/特殊字符的路径）────────────
# 使用数组而非字符串拼接 + eval，避免：
#   1. 路径含空格时被 Shell 分词成多个参数
#   2. 路径含 ;、&&、`、$() 等时被 eval 当成 Shell 命令执行
PYTEST_ARGS=(pytest)

# ── 并行执行参数（pytest-xdist） ──────────────────────────────────────────────
# PARALLEL_WORKERS 取值说明：
#   未设置 / "0" / "false" → 不追加 -n，保持串行
#   "auto"                 → -n auto（按 CPU 核数自动分配，UI 测试建议用固定值）
#   数字（如 "4"）          → -n 4（固定 4 个并发进程）
# ⚠️  注意：SeleniumBase UI 测试使用 xdist 时，每个 worker 会独立启动一个 Chrome 进程
#   请确保节点内存充足（每个 Chrome 约消耗 300~500MB），建议最多不超过 CPU 核数
WORKERS="${PARALLEL_WORKERS:-0}"
if [ "${WORKERS}" != "0" ] && [ "${WORKERS}" != "false" ] && [ -n "${WORKERS}" ]; then
    PYTEST_ARGS+=(-n "${WORKERS}")
    echo "  并行模式: -n ${WORKERS}"
else
    echo "  串行模式（PARALLEL_WORKERS 未设置或为 0）"
fi

if [ -n "${SCRIPT_PATHS}" ]; then
    # 将逗号分隔的路径逐一追加为独立参数，每个路径作为一个数组元素
    # 路径格式：examples/E/test_xxx.py（相对于仓库根目录）
    IFS=',' read -ra RAW_PATHS <<< "${SCRIPT_PATHS}"
    for p in "${RAW_PATHS[@]}"; do
        # 去除首尾空格
        p="${p#"${p%%[![:space:]]*}"}"
        p="${p%"${p##*[![:space:]]}"}"
        if [ -n "$p" ]; then
            PYTEST_ARGS+=("${p}")
        fi
    done
elif [ -n "${MARKER}" ]; then
    PYTEST_ARGS+=(-m "${MARKER}")
fi

# 追加报告参数（每个参数独立成数组元素，路径中的特殊字符会被正确处理）
PYTEST_ARGS+=(
    --json-report
    "--json-report-file=${REPORT_FILE}"
    "--junitxml=${JUNIT_FILE}"
    -v
)

echo "  命令: ${PYTEST_ARGS[*]}"
echo ""

# 设置 ChromeDriver 路径，防止 SeleniumBase 运行时走外网下载
export PATH="/usr/local/bin:${PATH}"
export CHROMEDRIVER=/usr/local/bin/chromedriver
export SB_DRIVER_CACHE_PATH=/usr/local/bin

# 执行 pytest，捕获退出码（set +e 防止 set -eo 在有失败用例时终止脚本）
set +e
"${PYTEST_ARGS[@]}"
PYTEST_EXIT=$?
set -e

echo ""
if [ "${PYTEST_EXIT}" -eq 0 ]; then
    BUILD_STATUS="success"
    echo "  ✅ pytest 执行完成（全部通过）"
elif [ "${PYTEST_EXIT}" -eq 1 ]; then
    BUILD_STATUS="failed"
    echo "  ❌ pytest 执行完成（存在失败用例），exit code: ${PYTEST_EXIT}"
else
    BUILD_STATUS="failed"
    echo "  ❌ pytest 异常退出，exit code: ${PYTEST_EXIT}"
fi

# ── 5. 回调平台 ───────────────────────────────────────────────────────────────
echo ""
echo "▶ [5/5] 回调平台..."

END_MS=$(date +%s%3N)
DURATION_MS=$(( END_MS - START_MS ))

# ── 解析 test-report.json，构造含每条 case 结果的完整 payload ─────────────────
# 平台通过 results 数组更新每条用例的真实状态（passed/failed/skipped）
# 若只传 status 而不传 results，平台会将所有用例标为 failed/error
PAYLOAD=""
if [ -f "${REPORT_FILE}" ]; then
    echo "  解析 test-report.json，提取每条 case 结果..."
    # 用 Python（镜像内已有）解析 JSON 并构造回调 payload
    # set +e 防止 python3 失败时因 pipefail 导致整个脚本退出
    set +e
    PAYLOAD=$(python3 - <<PYEOF
import json, sys

try:
    with open("${REPORT_FILE}", "r", encoding="utf-8") as f:
        report = json.load(f)
except Exception as e:
    sys.stderr.write(f"Failed to read report: {e}\n")
    sys.exit(1)

summary = report.get("summary", {})
passed  = summary.get("passed", 0)
failed  = (summary.get("failed", 0) + summary.get("error", 0))
skipped = summary.get("skipped", 0)
total   = summary.get("total", passed + failed + skipped)

# 整体状态判断：
#   total=0 → error（未收集到任何用例，可能是路径错误或环境问题）
#   failed>0 → failed
#   全部通过  → success
if total == 0:
    overall_status = "error"
elif failed == 0:
    overall_status = "success"
else:
    overall_status = "failed"

results = []
for t in report.get("tests", []):
    outcome = str(t.get("outcome", "error")).lower()
    if outcome in ("passed",):
        status = "passed"
    elif outcome in ("failed", "error"):
        status = "failed"
    elif outcome in ("skipped",):
        status = "skipped"
    else:
        status = "error"

    node_id = str(t.get("nodeid", ""))
    duration_ms = int(round(float(t.get("duration", 0)) * 1000))

    # 提取错误信息（longrepr 可能是字符串或对象）
    longrepr = t.get("longrepr", None)
    error_msg = None
    if isinstance(longrepr, str) and longrepr.strip():
        error_msg = longrepr.strip()[:2000]
    elif isinstance(longrepr, dict):
        reprcrash = longrepr.get("reprcrash", {})
        if isinstance(reprcrash, dict):
            error_msg = reprcrash.get("message", "")[:2000]

    entry = {
        "caseId": 0,
        "caseName": node_id,
        "status": status,
        "duration": duration_ms,
    }
    if error_msg:
        entry["errorMessage"] = error_msg

    results.append(entry)

payload = {
    "runId": ${RUN_ID},
    "status": overall_status,
    "passedCases": passed,
    "failedCases": failed,
    "skippedCases": skipped,
    "durationMs": ${DURATION_MS},
    "results": results,
}

print(json.dumps(payload, ensure_ascii=False))
PYEOF
)
    PYTHON_EXIT=$?
    set -e
    if [ ${PYTHON_EXIT} -ne 0 ] || [ -z "${PAYLOAD}" ]; then
        echo "  ⚠ test-report.json 解析失败，降级为仅传汇总状态"
        PAYLOAD="{\"runId\":${RUN_ID},\"status\":\"${BUILD_STATUS}\",\"durationMs\":${DURATION_MS}}"
    else
        # 一次 Python 调用提取全部统计数，避免三次启动进程
        read -r PARSED_PASSED PARSED_FAILED PARSED_TOTAL <<< "$(python3 -c "
import json, sys
try:
    d = json.loads(sys.stdin.read())
    print(d.get('passedCases',0), d.get('failedCases',0), len(d.get('results',[])))
except Exception:
    print('? ? ?')
" <<< "${PAYLOAD}" 2>/dev/null || echo '? ? ?')"
        echo "  ✅ 解析完成: passed=${PARSED_PASSED} failed=${PARSED_FAILED} total=${PARSED_TOTAL}"
    fi
else
    echo "  ⚠ 未找到 ${REPORT_FILE}，降级为仅传汇总状态"
    PAYLOAD="{\"runId\":${RUN_ID},\"status\":\"${BUILD_STATUS}\",\"durationMs\":${DURATION_MS}}"
fi

echo "  payload 长度: ${#PAYLOAD} 字节"

# 将 payload 写入临时文件，避免 shell 展开时对 JSON 中特殊字符（$、`、! 等）的误处理
PAYLOAD_FILE="/tmp/cb_payload_${RUN_ID}.json"
printf '%s' "${PAYLOAD}" > "${PAYLOAD_FILE}"

CALLBACK_OK=0
for attempt in 1 2 3; do
    HTTP_CODE=$(curl -sS \
        -o /tmp/cb_response_${attempt}.txt \
        -w '%{http_code}' \
        -X POST "${CALLBACK_URL}" \
        -H 'Content-Type: application/json' \
        --connect-timeout 10 \
        --max-time 30 \
        -k \
        --data-binary "@${PAYLOAD_FILE}" \
    )
    CURL_EXIT=$?
    RESPONSE_BODY=$(cat /tmp/cb_response_${attempt}.txt 2>/dev/null || echo "")

    echo "  attempt=${attempt} curl_exit=${CURL_EXIT} http_code=${HTTP_CODE}"
    [ -n "${RESPONSE_BODY}" ] && echo "  response: ${RESPONSE_BODY}"

    if [ "${CURL_EXIT}" -eq 0 ] && { [ "${HTTP_CODE}" = "200" ] || [ "${HTTP_CODE}" = "202" ]; }; then
        CALLBACK_OK=1
        echo "  ✅ 回调成功"
        break
    fi

    # 4xx 客户端错误（非 429）不重试
    if [ "${CURL_EXIT}" -eq 0 ] && echo "${HTTP_CODE}" | grep -qE '^4[^2][0-9]$'; then
        echo "  4xx 客户端错误，不再重试"
        break
    fi

    if [ "${attempt}" -lt 3 ]; then
        SLEEP_SEC=$(( attempt * 3 ))
        echo "  等待 ${SLEEP_SEC}s 后重试..."
        sleep "${SLEEP_SEC}"
    fi
done

if [ "${CALLBACK_OK}" -ne 1 ]; then
    echo "  ⚠ 回调最终失败，平台将通过轮询兜底同步结果"
fi

# 清理临时 payload 文件
rm -f "${PAYLOAD_FILE:-}" /tmp/cb_response_*.txt

echo ""
echo "══════════════════════════════════════════════════════"
echo "  执行完成  状态=${BUILD_STATUS}  耗时=${DURATION_MS}ms"
echo "══════════════════════════════════════════════════════"

# 以 pytest 退出码决定容器退出状态
# Jenkins 通过容器退出码判断 stage 成败
exit "${PYTEST_EXIT}"
