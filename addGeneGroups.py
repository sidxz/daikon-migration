from apiClient import getGeneGroups
from apiClient import getGenesWithAccessionKey
from apiClient import addGeneGroup
import pprint

GeneGroupsRaw = [
    {
        "name": "PrcBA",
        "type": "protein-complex",
        "genes": [
            {
                "accessionNumber": "Rv2109c",
            },
            {
                "accessionNumber": "Rv2110c",
            }
        ]
    },
    {
        "name": "RNA-Pol-Sig-A",
        "type": "protein-complex",
        "genes": [
            {
                "accessionNumber": "Rv0668",
            },
            {
                "accessionNumber": "Rv2703",
            },
            {
                "accessionNumber": "Rv1390",
            },
            {
                "accessionNumber": "Rv0667",
            },
            {
                "accessionNumber": "Rv3457c",
            }
        ]
    },
    {
        "name": "ClpP1P2",
        "type": "protein-complex",
        "genes": [
            {
                "accessionNumber": "Rv2460c",
            },
            {
                "accessionNumber": "Rv2461c",
            }
        ]
    },
    {
        "name": "CydAB",
        "type": "protein-complex",
        "genes": [
            {
                "accessionNumber": "Rv1622c",
            },
            {
                "accessionNumber": "Rv1623c",
            }
        ]
    },
    {
        "name": "HadAB",
        "type": "protein-complex",
        "genes": [
            {
                "accessionNumber": "Rv0635",
            },
            {
                "accessionNumber": "Rv0636",
            }
        ]
    },
    {
        "name": "TrpAB",
        "type": "protein-complex",
        "genes": [
            {
                "accessionNumber": "Rv1612",
            },
            {
                "accessionNumber": "Rv1613",
            }
        ]
    },
    {
        "name": "HadBC",
        "type": "protein-complex",
        "genes": [
            {
                "accessionNumber": "Rv0636",
            },
            {
                "accessionNumber": "Rv0637",
            }
        ]
    },
    {
        "name": "GyrAB",
        "type": "protein-complex",
        "genes": [
            {
                "accessionNumber": "Rv0005",
            },
            {
                "accessionNumber": "Rv0006",
            }
        ]
    },
    {
        "name": "PheST",
        "type": "protein-complex",
        "genes": [
            {
                "accessionNumber": "Rv1650",
            },
            {
                "accessionNumber": "Rv1649",
            }
        ]
    },
    {
        "name": "RNA-Pol-Core",
        "type": "protein-complex",
        "genes": [
            {
                "accessionNumber": "Rv0668",
            },
            {
                "accessionNumber": "Rv1390",
            },
            {
                "accessionNumber": "Rv0667",
            },
            {
                "accessionNumber": "Rv3457c",
            }
        ]
    },
    {
        "name": "HsaAB",
        "type": "protein-complex",
        "genes": [
            {
                "accessionNumber": "Rv3567c",
            },
            {
                "accessionNumber": "Rv3570c",
            }
        ]
    },
    {
        "name": "AHAS",
        "type": "protein-complex",
        "genes": [
            {
                "accessionNumber": "Rv3002c",
            },
            {
                "accessionNumber": "Rv3470c",
            }
        ]
    },
    {
        "name": "Anthranilate-synthetase",
        "type": "protein-complex",
        "genes": [
            {
                "accessionNumber": "Rv0013",
            },
            {
                "accessionNumber": "Rv1609",
            }
        ]
    },
    {
        "name": "ATP-synthase",
        "type": "protein-complex",
        "genes": [
            {
                "accessionNumber": "Rv1305",
            },
            {
                "accessionNumber": "Rv1658",
            },
            {
                "accessionNumber": "Rv1699",
            },
            {
                "accessionNumber": "Rv1306",
            },
            {
                "accessionNumber": "Rv1307",
            },
            {
                "accessionNumber": "Rv1308",
            },
            {
                "accessionNumber": "Rv1309",
            },
            {
                "accessionNumber": "Rv1310",
            },
            {
                "accessionNumber": "Rv1311",
            },
            {
                "accessionNumber": "Rv0803",
            }
        ]
    },
    {
        "name": "Bc1-Complex",
        "type": "protein-complex",
        "genes": [
            {
                "accessionNumber": "Rv2196",
            },
            {
                "accessionNumber": "Rv3316",
            },
            {
                "accessionNumber": "Rv2200c",
            },
            {
                "accessionNumber": "Rv3043c",
            }
        ]
    },
    {
        "name": "Cytochrome-BD",
        "type": "protein-complex",
        "genes": [
            {
                "accessionNumber": "Rv1622c",
            },
            {
                "accessionNumber": "Rv1623c",
            },

        ]
    },
    {
        "name": "D-ala-D-ala",
        "type": "protein-complex",
        "genes": [
            {
                "accessionNumber": "Rv2981c",
            },
            {
                "accessionNumber": "Rv2911",
            },
            {
                "accessionNumber": "Rv3330",
            },
        ]
    },
    {
        "name": "DNA-Gyrase",
        "type": "protein-complex",
        "genes": [
            {
                "accessionNumber": "Rv0005",
            },
            {
                "accessionNumber": "Rv0006",
            },
        ]
    },
    {
        "name": "DNA-Polymerase",
        "type": "protein-complex",
        "genes": [
            {
                "accessionNumber": "Rv3644c",
            },
            {
                "accessionNumber": "Rv1629",
            },
            {
                "accessionNumber": "Rv3711c",
            },
            {
                "accessionNumber": "Rv0002",
            },
            {
                "accessionNumber": "Rv1547",
            },
            {
                "accessionNumber": "Rv3370c",
            },
            {
                "accessionNumber": "Rv2343c",
            },
            {
                "accessionNumber": "Rv1537",
            },
            {
                "accessionNumber": "Rv3721c",
            },
            {
                "accessionNumber": "Rv1259",
            }
        ]
    },
    {
        "name": "DprE1-MoeW-Dual",
        "type": "protein-complex",
        "genes": [
            {
                "accessionNumber": "Rv3790",
            },
            {
                "accessionNumber": "Rv2338c",
            },
        ]
    },
    {
        "name": "IMPDH",
        "type": "protein-complex",
        "genes": [
            {
                "accessionNumber": "Rv1843c",
            },
            {
                "accessionNumber": "Rv3410c",
            },
            {
                "accessionNumber": "Rv3411c",
            },
        ]
    },
    {
        "name": "KatG-InhA-Dual",
        "type": "protein-complex",
        "genes": [
            {
                "accessionNumber": "Rv1484",
            },
            {
                "accessionNumber": "Rv1908c",
            }
        ]
    },
    {
        "name": "MmaA",
        "type": "protein-complex",
        "genes": [
            {
                "accessionNumber": "Rv0642c",
            },
            {
                "accessionNumber": "Rv0643c",
            },
            {
                "accessionNumber": "Rv0644c",
            },
            {
                "accessionNumber": "Rv0645c",
            },
        ]
    },
    {
        "name": "MmaA",
        "type": "protein-complex",
        "genes": [
            {
                "accessionNumber": "Rv0642c",
            },
            {
                "accessionNumber": "Rv0643c",
            },
            {
                "accessionNumber": "Rv0644c",
            },
            {
                "accessionNumber": "Rv0645c",
            },
        ]
    },
    {
        "name": "PBP",
        "type": "protein-complex",
        "genes": [
            {
                "accessionNumber": "Rv1730c",
            },
            {
                "accessionNumber": "Rv2864c",
            },
            {
                "accessionNumber": "Rv0016c",
            },
            {
                "accessionNumber": "Rv2163c",
            },
            {
                "accessionNumber": "Rv0050",
            },
            {
                "accessionNumber": "Rv3682",
            },
            {
                "accessionNumber": "Rv1110",
            },
            {
                "accessionNumber": "Rv3382c",
            },
            {
                "accessionNumber": "Rv2911",
            },
            {
                "accessionNumber": "Rv3330",
            }
        ]
    },
    {
        "name": "PheRS",
        "type": "protein-complex",
        "genes": [
            {
                "accessionNumber": "Rv1649",
            },
            {
                "accessionNumber": "Rv1650",
            }
        ]
    },
    {
        "name": "Ribosome",
        "type": "protein-complex",
        "genes": [
            {
                "accessionNumber": "Rv2058c",
            },
            {
                "accessionNumber": "Rv0995",
            },
            {
                "accessionNumber": "Rv3420c",
            },
            {
                "accessionNumber": "Rv0053",
            },
            {
                "accessionNumber": "Rv0718",
            },
            {
                "accessionNumber": "Rv0723",
            },
            {
                "accessionNumber": "Rv0640",
            },
            {
                "accessionNumber": "Rv0714",
            },
            {
                "accessionNumber": "Rv2412",
            },
            {
                "accessionNumber": "Rv3458c",
            }
        ]
    },
    {
        "name": "PrrAB",
        "type": "protein-complex",
        "genes": [
            {
                "accessionNumber": "Rv0903c",
            },
            {
                "accessionNumber": "Rv0902c",
            }
        ]
    },
    {
        "name": "RNA-polymerase",
        "type": "protein-complex",
        "genes": [
            {
                "accessionNumber": "Rv2710",
            },
            {
                "accessionNumber": "Rv0445c",
            },
            {
                "accessionNumber": "Rv0735",
            },
            {
                "accessionNumber": "Rv1189",
            },
            {
                "accessionNumber": "Rv1221",
            },
            {
                "accessionNumber": "Rv2069",
            },
            {
                "accessionNumber": "Rv2703",
            },
            {
                "accessionNumber": "Rv3286c",
            },
            {
                "accessionNumber": "Rv3911",
            },
            {
                "accessionNumber": "Rv0667",
            }
        ]
    },
    {
        "name": "Cytochrome-BC",
        "type": "protein-complex",
        "genes": [
            {
                "accessionNumber": "Rv2196",
            },
            {
                "accessionNumber": "Rv3316",
            },
            {
                "accessionNumber": "Rv2200c",
            },
            {
                "accessionNumber": "Rv3043c",
            }
        ]
    },
    {
        "name": "ATP-Synthesis",
        "type": "protein-complex",
        "genes": [
            {
                "accessionNumber": "Rv1305",
            },
            {
                "accessionNumber": "Rv1658",
            },
            {
                "accessionNumber": "Rv1699",
            },
            {
                "accessionNumber": "Rv1306",
            },
            {
                "accessionNumber": "Rv1307",
            },
            {
                "accessionNumber": "Rv1308",
            },
            {
                "accessionNumber": "Rv1309",
            },
            {
                "accessionNumber": "Rv1310",
            },
            {
                "accessionNumber": "Rv1311",
            },
            {
                "accessionNumber": "Rv0803",
            }
        ]
    },
]


print("# -------------------------------------------")
print("# Fetch : Existing Gene Groups")
existingGeneGroups = getGeneGroups()
print("# Fetch: Genes")
genes = getGenesWithAccessionKey()

GeneGroupsConverted = []

print("# Transform: GeneGroups")

for geneGroupRaw in GeneGroupsRaw:
  if geneGroupRaw["name"] not in existingGeneGroups:
    geneIds = []
    for groupGenes in geneGroupRaw["genes"]:
      geneIds.append(
          {
              "GeneId": genes.get(groupGenes["accessionNumber"])["id"]
          }
      )

    GeneGroupsConverted.append(
        {
            "name": geneGroupRaw["name"],
            "type": "protein-complex",
            "genes": geneIds
        }
    )

print("# Will add")
pprint.pprint(GeneGroupsConverted)

success = 0
attempted = len(GeneGroupsConverted)
print("# Starting POST")
for geneGroupToAdd in GeneGroupsConverted:
  print(f"# Adding {geneGroupToAdd['name']} ....")
  res = addGeneGroup(geneGroupToAdd)
  print(f"# {res}")
  if res == 200:
    success = success + 1

print("=========SUMMARY===========")
print(f"TOTAL ATTEMPTED     : {attempted}")
print(f"SUCCESS             : {success}")
fail = attempted - success
print(f"FAIL                : {fail}")
percent = (success/attempted)*100 if attempted != 0 else 0
print(f"SUCCESS %        : {percent:.2f}")
