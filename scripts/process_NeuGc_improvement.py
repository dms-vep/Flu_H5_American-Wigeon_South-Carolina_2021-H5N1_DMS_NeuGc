"""Gets mutations that increase NeuGc usage."""


import pandas as pd


sys.stderr = sys.stdout = open(snakemake.log[0], "w")

(
    pd.read_csv(snakemake.input.csv)[
        [
            "wildtype",
            "site",
            "mutant",
            "difference",
            "difference_std",
            "times_seen",
            "fraction_pairs_w_mutation",
            "CMAH entry effect",
            "293 entry effect",
        ]
    ]
    .assign(
        increase_NeuGc_usage=lambda x: x["difference"].clip(lower=0).where(
            x["CMAH entry effect"] > 0, 0,
        ),
        increase_NeuGc_usage_std=lambda x: x["difference_std"].where(
            x["increase_NeuGc_usage"] > 0, 0,
        ),
    )
    .rename(columns={"fraction_pairs_w_mutation": "frac_models"})
    .to_csv(snakemake.output.csv, index=False)
)
