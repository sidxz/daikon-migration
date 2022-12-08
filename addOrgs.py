from apiClient import addAppOrg
from apiClient import getAppOrgs

import json


AppOrgsList = [
    {
        "name": "Texas A&M",
        "alias": "TAMU",
    },
    {
        "name": "AbbVie",
        "alias": "AbbVie",
    },
    {
        "name": "Calibr at Scripps",
        "alias": "Calibr",
    },
    {
        "name": "Colorado State University",
        "alias": "CSU",
    },
    {
        "name": "University of Dundee Drug Discovery Unit",
        "alias": "DDU",
    },
    {
        "name": "Eisai",
        "alias": "Eisai",
    },
    {
        "name": "Evotec",
        "alias": "Evotec",
    },
    {
        "name": "Global Health Drug Discovery Institute",
        "alias": "GHDDI",
    },
    {
        "name": "GlaxoSmithKline",
        "alias": "GSK",
    },
    {
        "name": "Hackensack Meridian Health Center for Discovery and Innovation",
        "alias": "HMH-CDI",
    },
    {
        "name": "Harvard School of Public Health",
        "alias": "HSPH",
    },
    {
        "name": "Janssen",
        "alias": "Janssen",
    },
    {
        "name": "LGenia",
        "alias": "LGenia",
    },
    {
        "name": "Merck Sharpe & Dohme",
        "alias": "MSD",
    },
    {
        "name": "National Institute of Allergy and Infectious Diseases",
        "alias": "NIAID",
    },
    {
        "name": "Seattle Children's Hospital",
        "alias": "SCH",
    },
    {
        "name": "TB Alliance",
        "alias": "TBA",
    },
    {
        "name": "Tufts University",
        "alias": "Tufts",
    },
    {
        "name": "University of Cape Town-Drug Discovery and Development Center",
        "alias": "UCT-H3D",
    },
    {
        "name": "University of Cape Town-Institute of Infectious Disease and Molecular Medicine",
        "alias": "UCT-IMD",
    },
    {
        "name": "Weill Cornell Medicine",
        "alias": "WCM",
    },
    {
        "name": "Bill & Melinda Gates Medical Research Institute",
        "alias": "GatesMRI",
    },
    {
        "name": "Sanofi",
        "alias": "Sanofi",
    },
    {
        "name": "Merck",
        "alias": "Merck",
    },
    {
        "name": "University of Dundee",
        "alias": "Dundee",
    },
    {
        "name": "University of Cape Town",
        "alias": "UCT",
    },
    {
        "name": "LIA",
        "alias": "LIA",
    },
    {
        "name": "Lilly",
        "alias": "Lilly",
    },
    {
        "name": "Unassigned/Unknown",
        "alias": "NA",
    }
]

print("# ========= ADD ORGS START =============")

existingAppOrgs = getAppOrgs()

for appOrg in AppOrgsList:
    if appOrg['alias'].upper() not in existingAppOrgs:
      print("# ---------ADDING-------")
      print(appOrg)
      print(addAppOrg(appOrg))

print("=========COMPLETE=============")