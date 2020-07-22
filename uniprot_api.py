#!/usr/bin/env python

import io
import os
import sys, argparse
import pandas as pd
import urllib.parse
import urllib.request

def script_usage():
    print('uniprot_api.py arguments:')
    print('\n Search database:')
    print('--query query UniProt database by <UniProt ID or file with list of IDs>')
    print('usage example: uniprot_api.py --query <query; eg. "Repair"> ')
    print('\n Retrieve data:')
    print('-r | --retrieve data for a given ID -q | --query <entries> and -f | --format <eg. "tab", "xml", "html", "xls", "fasta"> ')
    print('usage example: uniprot_api.py --retrieve --query "P86784" --format "tab"')
    print('Query syntax:')
    print('Entries containing two or more terms: human antigen | human AND antigen | human && antigen')
    print('Entries containing both terms in the exact order: "human antigen"')
    print('Entries containing one term but not the other: human NOT antigen | human !antigen')
    print('Entries containing either term: human OR mouse | human || mouse')
    print('Using parentheses to override boolean precedence rules: antigen AND (human OR mouse)')
    print('Entries containing terms starting with regular expression: anti*')
    print('Citations that have an author whose name starts with Tiger: author:Tiger* ')
    print('Entries with a sequence of at least 100 amino acids: length:[100 TO *] ')
    print('\n Convert Identifiers:')
    print('-c | --convert <database_abbreviation> from/to -t | --targetdb <database_abbreviation> the following ID(s) -q | --query <ID or filename with IDs> and -f | --format <eg. "tab", "xml", "html", "xls", "fasta">')
    print('usage example: uniprot_api.py --convert "ACC" --targetdb "P_ENTREZGENEID" --query "P86784" --format "tab"')

# Uniprot Base URLs
# Convert API
urlBatchConv = "https://www.uniprot.org/uploadlists/"
# Search API
urlSearch = "https://www.uniprot.org/uniprot/?"

# Convert Function
# Allows user to convert IDs within Uniprot database through REST API
# Details and database identifiers: https://www.uniprot.org/help/api_idmapping
# From: Database ID abbreviation
# To: Database ID abbreviation
# Format: html | tab | xls | fasta | gff | txt | xml | rdf | list | rss
# Query: Database identifier(s)
def convParameters(_from,to,format,query):
    parameters = {
    'from': _from,
    'to': to,
    'format': format,
    'query': query
    }

    return(parameters)

# Search function
# Allows user to query Uniprot database through REST API
# Details: https://www.uniprot.org/help/api_queries
# Columns: https://www.uniprot.org/help/uniprotkb_column_names
# Search syntax: https://www.uniprot.org/help/text-search
# Query: see Search syntax and columns links
# Format: html | tab | xls | fasta | gff | txt | xml | rdf | list | rss
# Include: yes | no - Include isoform sequences when the format parameter is set to fasta. (only works for rdf, ignored for all other format values)
# Compress: yes | no - Return results gzipped
# Limit: integer - Maximum number of results to retrieve.
# Offset: integer - Offset of the first result, typically used together with the limit parameter.
# Limit and ofsset arguments are not enabled in the script and will be passed as NULL as default
def searchParameters(query,format,columns,include,compress,limit,offset):
    parameters = {
    'query': query,
    'format': format,
    'columns': columns,
    'include': include,
    'compress': compress,
    'limit': limit,
    'offset': offset
    }
    return(parameters)

# API access function
def apiAccess(url,params):
    data = urllib.parse.urlencode(params)
    data = data.encode('utf-8')
    req = urllib.request.Request(url, data)
    print(req)
    with urllib.request.urlopen(req) as f:
       response = f.read()
    print(response.decode('utf-8'))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
            prog='Uniprot Access API handler',
            description='This script was developed to convert among datasets IDs and to retrieve data from Uniprot databases using REST API.',
            epilog='Dependencies: pyhton3; pandas; urllib. Run: python3 uniprot_api.py (without any arguments to see usage examples)'
    )
    parser.add_argument('-c', '--convert', help='convert entries from database <db> ', choices=['ACC+ID', 'ACC', 'ID', 'UPARC', 'NF50', 'NF90', 'NF100', 'GENENAME', 'CRC64', 'EMBL_ID', 'EMBL', 'P_ENTREZGENEID', 'P_GI', 'PIR', 'REFSEQ_NT_ID', 'P_REFSEQ_AC', 'PDB_ID', 'BIOGRID_ID', 'COMPLEXPORTAL_ID', 'DIP_ID', 'STRING_ID', 'CHEMBL_ID', 'DRUGBANK_ID', 'GUIDETOPHARMACOLOGY_ID', 'SWISSLIPIDS_ID', 'ALLERGOME_ID', 'CLAE_ID', 'ESTHER_ID', 'MEROPS_ID', 'PEROXIBASE_ID', 'REBASE_ID', 'TCDB_ID',  'GLYCONNECT_ID', 'BIOMUTA_ID', 'DMDM_ID', 'WORLD_2DPAGE_ID', 'CPTAC_ID', 'PROTEOMICSDB_ID', 'DNASU_ID', 'ENSEMBL_ID', 'ENSEMBL_PRO_ID', 'ENSEMBL_TRS_ID', 'ENSEMBLGENOME_ID', 'ENSEMBLGENOME_PRO_ID', 'ENSEMBLGENOME_TRS_ID', 'GENEDB_ID', 'P_ENTREZGENEID', 'KEGG_ID', 'PATRIC_ID', 'UCSC_ID', 'VECTORBASE_ID', 'WBPARASITE_ID', 'ARACHNOSERVER_ID', 'ARAPORT_ID', 'CCDS_ID', 'CGD', 'CONOSERVER_ID', 'DICTYBASE_ID', 'ECHOBASE_ID', 'EUHCVDB_ID', 'EUPATHDB_ID', 'FLYBASE_ID', 'GENECARDS_ID', 'GENEREVIEWS_ID', 'HGNC_ID', 'LEGIOLIST_ID', 'LEPROMA_ID', 'MAIZEGDB_ID', 'MGI_ID', 'MIM_ID', 'NEXTPROT_ID', 'ORPHANET_ID', 'PHARMGKB_ID', 'POMBASE_ID', 'PSEUDOCAP_ID', 'RGD_ID', 'SGD_ID', 'TUBERCULIST_ID', 'VGNC_ID', 'WORMBASE_ID', 'WORMBASE_PRO_ID', 'WORMBASE_TRS_ID', 'XENBASE_ID', 'ZFIN_ID', 'EGGNOG_ID', 'GENETREE_ID', 'HOGENOM_ID', 'KO_ID', 'OMA_ID', 'ORTHODB_ID', 'TREEFAM_ID', 'BIOCYC_ID', 'PLANT_REACTOME_ID', 'REACTOME_ID', 'UNIPATHWAY_ID', 'COLLECTF_ID', 'DISPROT_ID', 'IDEAL_ID', 'CHITARS_ID', 'GENEWIKI_ID', 'GENOMERNAI_ID', 'PHI_BASE_ID'])
    parser.add_argument('-t', '--to', help='convert entries to database <db>', choices=['ACC', 'ID', 'UPARC', 'NF50', 'NF90', 'NF100', 'GENENAME', 'CRC64', 'EMBL_ID', 'EMBL', 'P_ENTREZGENEID', 'P_GI', 'PIR', 'REFSEQ_NT_ID', 'P_REFSEQ_AC', 'PDB_ID', 'BIOGRID_ID', 'COMPLEXPORTAL_ID', 'DIP_ID', 'STRING_ID', 'CHEMBL_ID', 'DRUGBANK_ID', 'GUIDETOPHARMACOLOGY_ID', 'SWISSLIPIDS_ID', 'ALLERGOME_ID', 'CLAE_ID', 'ESTHER_ID', 'MEROPS_ID', 'PEROXIBASE_ID', 'REBASE_ID', 'TCDB_ID',  'GLYCONNECT_ID', 'BIOMUTA_ID', 'DMDM_ID', 'WORLD_2DPAGE_ID', 'CPTAC_ID', 'PROTEOMICSDB_ID', 'DNASU_ID', 'ENSEMBL_ID', 'ENSEMBL_PRO_ID', 'ENSEMBL_TRS_ID', 'ENSEMBLGENOME_ID', 'ENSEMBLGENOME_PRO_ID', 'ENSEMBLGENOME_TRS_ID', 'GENEDB_ID', 'P_ENTREZGENEID', 'KEGG_ID', 'PATRIC_ID', 'UCSC_ID', 'VECTORBASE_ID', 'WBPARASITE_ID', 'ARACHNOSERVER_ID', 'ARAPORT_ID', 'CCDS_ID', 'CGD', 'CONOSERVER_ID', 'DICTYBASE_ID', 'ECHOBASE_ID', 'EUHCVDB_ID', 'EUPATHDB_ID', 'FLYBASE_ID', 'GENECARDS_ID', 'GENEREVIEWS_ID', 'HGNC_ID', 'LEGIOLIST_ID', 'LEPROMA_ID', 'MAIZEGDB_ID', 'MGI_ID', 'MIM_ID', 'NEXTPROT_ID', 'ORPHANET_ID', 'PHARMGKB_ID', 'POMBASE_ID', 'PSEUDOCAP_ID', 'RGD_ID', 'SGD_ID', 'TUBERCULIST_ID', 'VGNC_ID', 'WORMBASE_ID', 'WORMBASE_PRO_ID', 'WORMBASE_TRS_ID', 'XENBASE_ID', 'ZFIN_ID', 'EGGNOG_ID', 'GENETREE_ID', 'HOGENOM_ID', 'KO_ID', 'OMA_ID', 'ORTHODB_ID', 'TREEFAM_ID', 'BIOCYC_ID', 'PLANT_REACTOME_ID', 'REACTOME_ID', 'UNIPATHWAY_ID', 'COLLECTF_ID', 'DISPROT_ID', 'IDEAL_ID', 'CHITARS_ID', 'GENEWIKI_ID', 'GENOMERNAI_ID', 'PHI_BASE_ID'])
    parser.add_argument('-v', '--version', action='version', version='%(prog) alpha 1.0')
    parser.add_argument('-q', '--query', help='search for words or IDs within Uniprot dabatabase (run uniprot_api.py without arguments to see query examples)')
    parser.add_argument('-f', '--format', choices=["html", "tab", "xls", "fasta", "gff", "txt", "xml", "rdf", "list", "rss"], default="tab")
    parser.add_argument('-r', '--retrieve', help='retrieve UniProt data for database entries/columns <Columns>', default="")
    parser.add_argument('-g', '--gzip', help='Return results gzipped', default="NO")
    parser.add_argument('-i', '--include', help='Include isoform sequences when the format parameter is set to fasta? Only works with RDF format', default="NO")
    parser.add_argument('-l', '--limit', help='Maximum number of results to retrieve', type=int, default="NULL")
    parser.add_argument('-s', '--offset', help='Offset of the first result, typically used together with the limit parameter',  type=int, default="NULL")
    if len(sys.argv)==1:
        script_usage()
        parser.print_help(sys.stderr)
        sys.exit(1)
    args = parser.parse_args()
    if args.convert and args.to and args.query and args.format :
        params = convParameters(args.convert, args.to, args.format, args.query)
        apiAccess(urlBatchConv, params)
    elif args.query and ar:
#        if not args.zip:
#            args.zip = "NO"
#        if not args.limit:
#            args.limit = "NULL"
#        if not args.include:
#            args.include = "YES"
        params = searchParameters(args.query, args.format, args.retrieve, args.include, args.zip, args.limit, args.offset):
        apiAccess(urlSearch, params)
        params = searchParameters(args.query, args.format, args.retrieve):
        apiAccess(urlSearch, params)
    else:
        script_usage()
