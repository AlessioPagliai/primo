# Launch training runs strictly sequentially: each must reach its first "Learning iteration"
# line before the next one starts. This is the reliable pattern - fixed 90 s staggers still
# wedge when a boot runs long (4 of 6 round-3 launches froze mid-boot under contention).
param([string[]]$Tasks = @('WalkG1','RunPend','RunImpact','RunG1'), [int]$NumEnvs = 1024)

foreach ($w in $Tasks) {
    $ts = Get-Date -Format HHmmss
    $log = "C:\Users\WKS\Documents\humanoid\rl_full_isaac\training_runs\r3_${w}_$ts.log"
    cmd /c "set OMNI_KIT_ACCEPT_EULA=YES&& set OMNI_CRASHREPORTER_ENABLED=0&& set PYTHONUNBUFFERED=1&& call C:\Users\WKS\isaac\env_isaaclab\Scripts\activate.bat && cd /d C:\Users\WKS\isaac\IsaacLab && start /min """" cmd /c ""call C:\Users\WKS\isaac\IsaacLab\isaaclab.bat -p scripts\reinforcement_learning\rsl_rl\train.py --task Isaac-Velocity-R3-$w-v0 --num_envs $NumEnvs --headless > $log 2>&1"""
    Write-Output "launched $w, waiting for first iteration..."
    $deadline = (Get-Date).AddMinutes(8)
    $started = $false
    while ((Get-Date) -lt $deadline) {
        Start-Sleep 15
        if (Select-String -Path $log -Pattern 'Learning iteration' -Quiet -ErrorAction SilentlyContinue) { $started = $true; break }
        if (Select-String -Path $log -Pattern 'Traceback' -Quiet -ErrorAction SilentlyContinue) { Write-Output "$w FAILED (traceback)"; break }
    }
    if ($started) { Write-Output "$w TRAINING" } else { Write-Output "$w did not start in 8 min - continuing anyway" }
}
Write-Output "SEQUENTIAL LAUNCH DONE"
