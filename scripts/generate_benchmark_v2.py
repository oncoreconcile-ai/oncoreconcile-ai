import csv
from pathlib import Path

OUT = Path("data/benchmark_v2.csv")

CASES = []

def add(case_id, input_disease, input_gene, input_variant,
        expected_disease, expected_gene, expected_variant,
        status, category, source="synthetic_curated", notes=""):
    CASES.append({
        "case_id": f"BV2_{case_id:04d}",
        "input_disease": input_disease,
        "input_gene": input_gene,
        "input_variant": input_variant,
        "expected_disease": expected_disease,
        "expected_gene": expected_gene,
        "expected_variant": expected_variant,
        "expected_status": status,
        "category": category,
        "source": source,
        "notes": notes,
    })

diseases = [
    ("NSCLC", "Lung Non-Small Cell Carcinoma", [
        ("EGFR", "Ex19del", "EGFR Exon 19 Deletion"),
        ("EGFR", "L858R", "EGFR L858R"),
        ("EGFR", "T790M", "EGFR T790M"),
        ("KRAS", "G12C", "KRAS G12C"),
        ("ALK", "fusion", "ALK Fusion"),
    ]),
    ("Breast Cancer", "Breast Carcinoma", [
        ("HER2", "amplification", "ERBB2 Amplification"),
        ("ERBB2", "amp", "ERBB2 Amplification"),
        ("PIK3CA", "H1047R", "PIK3CA H1047R"),
        ("BRCA1", "loss", "BRCA1 Loss"),
        ("TP53", "R273H", "TP53 R273H"),
    ]),
    ("AML", "Acute Myeloid Leukemia", [
        ("FLT3", "ITD", "FLT3 ITD"),
        ("IDH1", "R132H", "IDH1 R132H"),
        ("IDH2", "R172K", "IDH2 R172K"),
        ("NPM1", "mutation", "NPM1 Mutation"),
        ("RUNX1", "mutation", "RUNX1 Mutation"),
    ]),
    ("Colorectal Cancer", "Colorectal Carcinoma", [
        ("KRAS", "G12D", "KRAS G12D"),
        ("KRAS", "G12V", "KRAS G12V"),
        ("BRAF", "V600E", "BRAF V600E"),
        ("MSI", "high", "MSI-High"),
        ("NRAS", "Q61K", "NRAS Q61K"),
    ]),
    ("Melanoma", "Cutaneous Melanoma", [
        ("BRAF", "V600E", "BRAF V600E"),
        ("BRAF", "V600K", "BRAF V600K"),
        ("NRAS", "Q61R", "NRAS Q61R"),
        ("KIT", "mutation", "KIT Mutation"),
        ("NF1", "loss", "NF1 Loss"),
    ]),
]

aliases = {
    "NSCLC": ["NSCLC", "non small cell lung ca", "non-small cell lung cancer", "lung nsclc", "lung cancer"],
    "Breast Cancer": ["breast ca", "breast carcinoma", "HER2+ breast cancer", "TNBC", "breast cancer"],
    "AML": ["AML", "acute myeloid leukemia", "acute myelogenous leukemia", "myeloid leukemia", "AML disease"],
    "Colorectal Cancer": ["CRC", "colon cancer", "colorectal ca", "colorectal cancer", "rectal cancer"],
    "Melanoma": ["melanoma", "cutaneous melanoma", "skin melanoma", "malignant melanoma", "melanoma cancer"],
}

gene_aliases = {
    "EGFR": ["EGFR", "HER1", "ERBB1", "egfr", "Epidermal growth factor receptor"],
    "ERBB2": ["ERBB2", "HER2", "HER-2", "neu", "ERBB-2"],
    "KRAS": ["KRAS", "K-RAS", "kras", "KRAS2", "Kirsten ras"],
    "BRAF": ["BRAF", "B-RAF", "braf", "BRAF1", "v-raf"],
    "FLT3": ["FLT3", "flk2", "CD135", "FLT-3", "flt3"],
    "IDH1": ["IDH1", "idh1", "IDH-1", "isocitrate dehydrogenase 1", "IDH1 gene"],
    "IDH2": ["IDH2", "idh2", "IDH-2", "isocitrate dehydrogenase 2", "IDH2 gene"],
    "TP53": ["TP53", "p53", "P53", "tumor protein p53", "TP-53"],
    "ALK": ["ALK", "ALK gene", "anaplastic lymphoma kinase", "ALK1", "alk"],
    "PIK3CA": ["PIK3CA", "PI3KCA", "p110 alpha", "PIK3CA gene", "pik3ca"],
    "BRCA1": ["BRCA1", "BRCA-1", "brca1", "breast cancer 1", "BRCA1 gene"],
    "NPM1": ["NPM1", "npm1", "nucleophosmin", "NPM", "NPM1 gene"],
    "RUNX1": ["RUNX1", "runx1", "AML1", "CBFA2", "RUNX1 gene"],
    "MSI": ["MSI", "microsatellite instability", "MSI-H", "MSI high", "msi"],
    "NRAS": ["NRAS", "N-RAS", "nras", "NRAS gene", "neuroblastoma RAS"],
    "KIT": ["KIT", "c-KIT", "CD117", "KIT gene", "kit"],
    "NF1": ["NF1", "neurofibromin 1", "NF-1", "nf1", "NF1 gene"],
}

variant_aliases = {
    "Ex19del": ["Ex19del", "ex19del", "exon 19 deletion", "EGFR exon19 del", "E19del"],
    "amplification": ["amplification", "amp", "amplified", "copy number gain", "CN gain"],
    "ITD": ["ITD", "internal tandem duplication", "FLT3-ITD", "itd", "FLT3 internal tandem duplication"],
    "fusion": ["fusion", "rearrangement", "translocation", "gene fusion", "fusion positive"],
    "high": ["high", "MSI-H", "MSI high", "microsatellite instability high", "MSI-high"],
    "mutation": ["mutation", "mut", "variant", "alteration", "mutated"],
    "loss": ["loss", "deletion", "LOF", "loss of function", "inactivation"],
}

case_id = 1

# 5 diseases × 5 variants × aliases = 500-ish
for disease_raw, disease_expected, variants in diseases:
    disease_inputs = aliases[disease_raw]
    for gene, variant_raw, variant_expected in variants:
        gene_inputs = gene_aliases.get(gene, [gene])
        variant_inputs = variant_aliases.get(variant_raw, [variant_raw, variant_raw.lower(), variant_raw.upper(), f"{gene} {variant_raw}", f"{gene}-{variant_raw}"])

        for i in range(4):
            add(
                case_id,
                disease_inputs[i % len(disease_inputs)],
                gene_inputs[i % len(gene_inputs)],
                variant_inputs[i % len(variant_inputs)],
                disease_expected,
                "ERBB2" if gene == "HER2" else gene,
                variant_expected,
                "AUTO_RECONCILE",
                "alias_or_exact",
                notes="Expected to reconcile automatically if local catalog supports it."
            )
            case_id += 1

# Add REVIEW_REQUIRED cases
review_cases = [
    ("AML", "IDH2", "R172K", "Acute Myeloid Leukemia", "IDH2", "IDH2 R172K"),
    ("NSCLC", "EGFR", "C797S", "Lung Non-Small Cell Carcinoma", "EGFR", "EGFR C797S"),
    ("Breast Cancer", "ESR1", "Y537S", "Breast Carcinoma", "ESR1", "ESR1 Y537S"),
    ("CRC", "KRAS", "A146T", "Colorectal Carcinoma", "KRAS", "KRAS A146T"),
]

while len(CASES) < 450:
    d, g, v, ed, eg, ev = review_cases[len(CASES) % len(review_cases)]
    add(case_id, d, g, v, ed, eg, ev, "REVIEW_REQUIRED", "external_or_review_required", notes="Expected to require reviewer evidence package.")
    case_id += 1

# Add CANNOT_RECONCILE noise cases
while len(CASES) < 500:
    add(
        case_id,
        "unknown cancer term",
        "FAKEGENE123",
        "unknown_variant",
        "",
        "",
        "",
        "CANNOT_RECONCILE",
        "negative_control",
        notes="Expected to fail safely without auto-reconciliation."
    )
    case_id += 1

OUT.parent.mkdir(exist_ok=True)

with OUT.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(CASES[0].keys()))
    writer.writeheader()
    writer.writerows(CASES)

print(f"Wrote {len(CASES)} cases to {OUT}")