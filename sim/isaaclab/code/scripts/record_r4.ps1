# Record feet-view Play videos for all six round-4 policies at model_2999.
$out = "C:\Users\WKS\Documents\humanoid\rl_full_isaac\training_runs\compare_r4"
New-Item -ItemType Directory -Force $out | Out-Null

foreach ($w in @('PendBase','PendShort','PendLow','PendSlow','ImpactShort','PendTrack')) {
    $exp = "r4_" + $w.ToLower()
    $dir = "C:\Users\WKS\isaac\IsaacLab\logs\rsl_rl\$exp"
    $run = Get-ChildItem $dir -Directory | Sort-Object Name | Select-Object -Last 1
    $ck  = Join-Path $run.FullName "model_2999.pt"
    if (-not (Test-Path $ck)) { Write-Output "$w : model_2999 missing"; continue }

    $log = "C:\Users\WKS\Documents\humanoid\rl_full_isaac\training_runs\play_r4_${w}.log"
    cmd /c "set OMNI_KIT_ACCEPT_EULA=YES&& set OMNI_CRASHREPORTER_ENABLED=0&& set PYTHONUNBUFFERED=1&& call C:\Users\WKS\isaac\env_isaaclab\Scripts\activate.bat && cd /d C:\Users\WKS\isaac\IsaacLab && call C:\Users\WKS\isaac\IsaacLab\isaaclab.bat -p scripts\reinforcement_learning\rsl_rl\play.py --task Isaac-Velocity-R4-$w-Play-v0 --num_envs 4 --video --video_length 1000 --headless --checkpoint $ck > $log 2>&1"

    $src = Join-Path $run.FullName "videos\play\rl-video-step-0.mp4"
    if (-not (Test-Path $src)) { Write-Output "$w : FAILED"; continue }
    do { $a = (Get-Item $src).Length; Start-Sleep 4; $b = (Get-Item $src).Length } while ($a -ne $b)
    Copy-Item $src (Join-Path $out "$w.mp4") -Force
    Write-Output ("{0} : ok {1} KB" -f $w, [int]($b/1KB))
}
Write-Output "ALL DONE"
