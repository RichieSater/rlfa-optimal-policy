import json

from rlfa_optimal_policy.cli import main


def test_characterize_n2_cli(capsys) -> None:
    status = main(["characterize-n2"])
    output = json.loads(capsys.readouterr().out)

    assert status == 0
    assert output["stopping_items_1_based"] == [1]
    assert output["literal_simplex_optimum"] == "1"
    assert output["full_support_infimum"] == "1"
    assert not output["full_support_attained"]
    assert output["oracle_expected_tau"] == "3/2"
    assert not output["oracle_is_globally_optimal"]


def test_characterize_box_cli(capsys) -> None:
    status = main(
        [
            "characterize-box",
            "--pi",
            "1/2",
            "1/3",
            "1/6",
            "--lower",
            "0",
            "0",
            "0",
            "--upper",
            "1",
            "1",
            "1",
            "--epsilon",
            "1/2",
            "--costs",
            "3",
            "2",
            "1",
        ]
    )
    output = json.loads(capsys.readouterr().out)
    assert status == 0
    assert output["minimum_reviews"] == 1
    assert output["optimal_prefix_1_based"] == [1]
    assert output["heterogeneous_cost_solution"]["total_cost"] == "3"
