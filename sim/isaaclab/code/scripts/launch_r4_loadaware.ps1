# Load-aware sequential launch of the six round-4 runs (same pattern that worked for round 3).
function Launch-Seq([string[]]$Tasks) {
    foreach ($w in $Tasks) {
        $ts = Get-Date -Format HHmmss
        $log = "C:\Users\WKS\Documents\humanoid\rl_full_isaac\training_runs\r4_${w}_$ts.log"
        cmd /c "set OMNI_KIT_ACCEPT_EULA=YES&& set OMNI_CRASHREPORTER_ENABLED=0&& set PYTHONUNBUFFERED=1&& call C:\Users\WKS\isaac\env_isaaclab\Scripts\activate.bat && cd /d C:\Users\WKS\isaac\IsaacLab && start /min """" cmd /c ""call C:\Users\WKS\isaac\IsaacLab\isaaclab.bat -p scripts\reinforcement_learning\rsl_rl\train.py --task Isaac-Velocity-R4-$w-v0 --num_envs 1024 --headless > $log 2>&1"""
        Write-Output "launched $w"
        $deadline = (Get-Date).AddMinutes(8); $ok = $false
        while ((Get-Date) -lt $deadline) {
            Start-Sleep 15
            if (Select-String -Path $log -Pattern 'Learning iteration' -Quiet -ErrorAction SilentlyContinue) { $ok = $true; break }
            if (Select-String -Path $log -Pattern 'Traceback' -Quiet -ErrorAction SilentlyContinue) { Write-Output "$w TRACEBACK"; break }
        }
        Write-Output ("{0} {1}" -f $w, $(if ($ok) {"TRAINING"} else {"NOT STARTED IN 8MIN"}))
    }
}

Write-Output "=== BATCH 1 ==="
Launch-Seq @('PendBase','PendShort','PendLow')
Start-Sleep 60
$g = (nvidia-smi --query-gpu=memory.used,temperature.gpu --format=csv,noheader,nounits) -split ',\s*'
$os = Get-CimInstance Win32_OperatingSystem
$ramFree = [math]::Round($os.FreePhysicalMemory/1MB,1)
Write-Output ("=== LOAD: GPU {0} MiB, {1} C; RAM free {2} GB" -f [int]$g[0],[int]$g[1],$ramFree)
if (([int]$g[0] -lt 60000) -and ([int]$g[1] -lt 80) -and ($ramFree -gt 60)) {
    Write-Output "=== GATE PASSED - BATCH 2 ==="
    Launch-Seq @('PendSlow','ImpactShort','PendTrack')
} else { Write-Output "=== GATE FAILED - BATCH 2 SKIPPED ===" }
Write-Output "R4 LAUNCH DONE"
