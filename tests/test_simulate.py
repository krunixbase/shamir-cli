from pathlib import Path

from shamir.core import split_secret
from utils.repo import save_shares, log_simulation
from utils.forensic import generate_resilience_report


def test_simulation_recoverable(tmp_path, monkeypatch):
    """
    Simulation should succeed when threshold is met.
    """
    monkeypatch.chdir(tmp_path)

    secret = b"simulate-ok"
    threshold = 2
    total_shares = 3
    label = "simok"

    shares = split_secret(secret, threshold=threshold, shares=total_shares)
    save_shares(shares, label=label)

    # simulate success
    log_simulation(
        label=label,
        total_shares=total_shares,
        threshold=threshold,
        used_shares=threshold,
        success=True,
    )

    log_dir = Path("artifacts/logs")
    logs = list(log_dir.glob("simulation.log"))

    assert len(logs) == 1
    assert "success" in logs[0].read_text()


def test_simulation_not_recoverable(tmp_path, monkeypatch):
    """
    Simulation should fail when threshold is not met.
    """
    monkeypatch.chdir(tmp_path)

    secret = b"simulate-fail"
    threshold = 3
    total_shares = 3
    label = "simfail"

    shares = split_secret(secret, threshold=threshold, shares=total_shares)
    save_shares(shares, label=label)

    log_simulation(
        label=label,
        total_shares=total_shares,
        threshold=threshold,
        used_shares=2,
        success=False,
    )

    log_dir = Path("artifacts/logs")
    logs = list(log_dir.glob("simulation.log"))

    assert len(logs) == 1
    assert "false" in logs[0].read_text().lower()


def test_resilience_report_generation(tmp_path, monkeypatch):
    """
    Resilience report should be generated without modifying shares.
    """
    monkeypatch.chdir(tmp_path)

    generate_resilience_report(
        label="resilience",
        total_shares=5,
        threshold=3,
        success=True,
    )

    forensic_dir = Path("artifacts/forensic")
    reports = list(forensic_dir.glob("*resilience*.txt"))

    assert len(reports) == 1
    content = reports[0].read_text()

    assert "RESILIENCE REPORT" in content
    assert "RECOVERABLE" in content
