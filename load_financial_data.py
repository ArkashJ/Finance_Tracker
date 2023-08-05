import requests
from config import * 
import data_store_and_inference as dsai
import pandas as pd

class LoadFinancialData:  
    def __init__(self):
        self.data = {}

    def download_data(self, api_endpoint):
        content = requests.get(api_endpoint)
        return content.json()

def list_of_companies():
    companies = {}
    company_name = ['Apple', 'Amazon', 'Microsoft', 
                    'Nvidia', 'Alphabet_ClassA', 
                    'Tesla', 'Meta Platforms', 'Alphabet_ClassC', 'Berkshire Hathaway Class_B'
                    'UnitedHealth Group'
                    ]
    company_symbol = ['AAPL', 'AMZN', 'MSFT',
                      'NVDA', 'GOOGL', 'TSLA', 'FB', 'GOOG', 'BRK.B', 'UNH'
                      ]
    len_company_name = len(company_name)
    for i in range(len_company_name):
        companies[company_name[i]] = company_symbol[i]
    return companies

def list_of_annual_statements():
    statements = ['income-statement', 'balance-sheet-statement', 'cash-flow-statement']
    return statements

def call_transcript():
    transcript = ['earning_call_transcript']
    return transcript

def make_endpoints():
    companies = list_of_companies()
    statements = list_of_annual_statements()
    endpoints = {}
    for company_name, company_symbol in companies.items():
        for statement in statements:
            api_endpoint = f'{URL}/{VERSION}/{statement}/{company_symbol}?apikey={FMP_KEY}&limit=120'
            if company_symbol in endpoints:
                endpoints[company_symbol].append(api_endpoint)
            else:
                endpoints[company_symbol] = [api_endpoint]
    return endpoints

def main():
    endpoints = make_endpoints()
    data_loader = LoadFinancialData()

    income_statements = {}
    balance_sheets = {}
    cash_flows = {}

    for symbol, endpoint_list in endpoints.items():
        for endpoint in endpoint_list:
            load_data = data_loader.download_data(endpoint)
            if "income-statement" in endpoint:
                income_statements[symbol] = pd.DataFrame(load_data)
            elif "balance-sheet-statement" in endpoint:
                balance_sheets[symbol] = pd.DataFrame(load_data)
            elif "cash-flow-statement" in endpoint:
                cash_flows[symbol] = pd.DataFrame(load_data)

    # Process income statements
    for symbol, income_statement in income_statements.items():
        company_name = symbol
        income_statement_store = dsai.DataStore(income_statement, company_name)
        income_statement_store.pre_process_data()
        income_statement_store.describe_data()
        if 'revenue' in income_statement_store.df.columns and 'netIncome' in income_statement_store.df.columns:
            income_statement_store.calculate_correlation('revenue', 'netIncome')
        if 'costOfRevenue' in income_statement_store.df.columns and 'grossProfit' in income_statement_store.df.columns:
            income_statement_store.calculate_correlation('costOfRevenue', 'grossProfit')
        if 'grossProfit' in income_statement_store.df.columns and 'operatingExpenses' in income_statement_store.df.columns:
            income_statement_store.calculate_correlation('grossProfit', 'operatingExpenses')
        income_statement_store.visualize_data(['revenue', 'grossProfit', 'netIncome'] )

    # Process balance sheets
    for symbol, balance_sheet in balance_sheets.items():
        company_name = symbol
        balance_sheet_store = dsai.DataStore(balance_sheet, company_name)
        balance_sheet_store.pre_process_data()
        balance_sheet_store.describe_data()
        
        if 'totalAssets' in balance_sheet_store.df.columns and 'totalLiabilities' in balance_sheet_store.df.columns:
            balance_sheet_store.calculate_correlation('totalAssets', 'totalLiabilities')
        if 'totalAssets' in balance_sheet_store.df.columns and 'totalStockholdersEquity' in balance_sheet_store.df.columns:
            balance_sheet_store.calculate_correlation('totalAssets', 'totalStockholdersEquity')
        if 'totalLiabilities' in balance_sheet_store.df.columns and 'totalStockholdersEquity' in balance_sheet_store.df.columns:
            balance_sheet_store.calculate_correlation('totalLiabilities', 'totalStockholdersEquity')
        balance_sheet_store.visualize_data(['totalAssets', 'totalLiabilities', 'totalStockholdersEquity'])

    # Process cash flows
    for symbol, cash_flow in cash_flows.items():
        company_name = symbol
        cash_flow_store = dsai.DataStore(cash_flow, company_name)
        cash_flow_store.pre_process_data()
        cash_flow_store.describe_data()
        if 'operatingCashflow' in cash_flow_store.df.columns and 'capitalExpenditure' in cash_flow_store.df.columns:
            cash_flow_store.calculate_correlation('operatingCashflow', 'capitalExpenditure')

main()

