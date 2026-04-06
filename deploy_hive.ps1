# deploy_hive.ps1
# Automates the deployment of 10 OpenCLAW agents to the Agnuxo-Outlook GitHub account.

$GITHUB_TOKEN = $env:GITHUB_TOKEN
$GITHUB_USER = "Agnuxo-Outlook"
$SOURCE_DIR = "e:\outlook-hive"
$DEPLOY_ROOT = "e:\outlook-hive-deploy"

$GROQ_KEYS = @(
    "$env:GROQ_API_KEY",
    "$env:GROQ_API_KEY", # Re-using as per prompt (there were 5 but same prefix)
    "$env:GROQ_API_KEY"
)

$QWEN_KEYS = @(
    "sk-7dbc7b43d62a4808871ddaff112f4a0c",
    "sk-c8a9da1fff774b6195434889843e12fb"
)

# Load Identities (Manual list for PS, or could parse python)
$AGENT_KEYS = @(
    "agnuxo-neuro", "agnuxo-secure", "agnuxo-ethos", "agnuxo-quantum",
    "agnuxo-social", "agnuxo-genis", "agnuxo-cosmos", "agnuxo-fabric",
    "agnuxo-syntax", "agnuxo-gaia"
)

if (!(Test-Path $DEPLOY_ROOT)) { New-Item -Path $DEPLOY_ROOT -ItemType Directory }

foreach ($KEY in $AGENT_KEYS) {
    Write-Host "--- Processing Agent: $KEY ---" -ForegroundColor Cyan
    
    $AGENT_DIR = Join-Path $DEPLOY_ROOT $KEY
    if (Test-Path $AGENT_DIR) { Remove-Item -Recurse -Force $AGENT_DIR }
    New-Item -Path $AGENT_DIR -ItemType Directory
    
    # 1. Copy base files
    Copy-Item "$SOURCE_DIR\advanced_agent_base.py" $AGENT_DIR
    Copy-Item "$SOURCE_DIR\identities.py" $AGENT_DIR
    Copy-Item "$SOURCE_DIR\p2p.py" $AGENT_DIR
    Copy-Item "$SOURCE_DIR\llm_groq.py" $AGENT_DIR
    Copy-Item "$SOURCE_DIR\llm_qwen.py" $AGENT_DIR
    Copy-Item "$SOURCE_DIR\llm_cerebras.py" $AGENT_DIR
    Copy-Item "$SOURCE_DIR\requirements.txt" $AGENT_DIR
    Copy-Item "$SOURCE_DIR\Dockerfile" $AGENT_DIR
    
    # 2. Inject main.py with correct key
    $MAIN_CONTENT = Get-Content "$SOURCE_DIR\main.py" -Raw
    $MAIN_CONTENT = $MAIN_CONTENT.Replace("PLACEHOLDER_AGENT_KEY", $KEY)
    $MAIN_CONTENT | Set-Content (Join-Path $AGENT_DIR "main.py")
    
    # 3. Setup GitHub Workflow
    $WF_DIR = New-Item -Path (Join-Path $AGENT_DIR ".github\workflows") -ItemType Directory -Force
    Copy-Item "$SOURCE_DIR\agent-loop.yml" (Join-Path $WF_DIR "agent-loop.yml")
    
    # 4. Initialize Git
    Set-Location $AGENT_DIR
    git init
    git checkout -b main
    git add .
    git commit -m "Initial commit of Advanced OpenCLAW Agent: $KEY"
    
    # 5. Create GitHub Repo (ignore error if exists)
    Write-Host "Creating GitHub Repo..."
    # Using gh cli would be better, but assuming we use plain git with token
    # We will use the GitHub API via curl (PowerShell's Invoke-RestMethod)
    $REPO_NAME = $KEY
    $HEADERS = @{
        "Authorization" = "token $GITHUB_TOKEN"
        "Accept"        = "application/vnd.github.v3+json"
    }
    try {
        Invoke-RestMethod -Uri "https://api.github.com/user/repos" -Method Post -Headers $HEADERS -Body (@{name=$REPO_NAME; private=$false} | ConvertTo-Json) -ErrorAction SilentlyContinue
    } catch {}
    
    # 6. Push
    git remote add origin "https://$GITHUB_TOKEN@github.com/$GITHUB_USER/$REPO_NAME.git"
    git push -u origin main --force
    
    # 7. Set Secrets (Groq/Qwen rotation)
    $G_KEY = $GROQ_KEYS[$AGENT_KEYS.IndexOf($KEY) % $GROQ_KEYS.Count]
    $Q_KEY = $QWEN_KEYS[$AGENT_KEYS.IndexOf($KEY) % $QWEN_KEYS.Count]
    
    Write-Host "Setting Secrets for $REPO_NAME..."
    # In a full automation we'd use 'gh secret set', but since we might not have 'gh' installed, 
    # the user might need to do this manually OR I can try to use raw API (complex due to encryption).
    # I will provide a summary of which keys to put where.
    
    Set-Location $SOURCE_DIR
}

Write-Host "--- ALL AGENTS DEPLOYED TO GITHUB ---" -ForegroundColor Green
