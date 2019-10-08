from neo4j import GraphDatabase
import csv

# Login credentials
user = "neo4j"
password = "password"

uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", password))

def process_account_data(tx, name, homedir, virtualpath_list):
    create_account_node(tx, name, homedir, virtualpath_list)
    create_path_node(tx, "/")
    create_path_nodes(tx, homedir)
    if virtualpath_list:
        for virtualpath in virtualpath_list:
            create_path_nodes(tx, virtualpath)

def create_account_node(tx, name, homedir, virtualpath_list):
    tx.run( "MERGE (n:account{name:$name, homedir:$homedir, virtualpath:$virtualpath})",
            name=name, homedir=homedir, virtualpath=virtualpath_list)

def create_path_nodes(tx, path):
    path_hierarchy = path.split("/")
    node_name = ""
    parent_node = "/"
    for node in path_hierarchy:
        if node:
            if parent_node == "/":
                node_name = parent_node + node
            else:
                node_name +=  "/" + node
            create_path_node(tx, node_name)
            tx.run( "MATCH (a:path),(b:path) WHERE a.name=$parent_node AND b.name=$node_name MERGE (a)-[r:contains]->(b)", 
                    parent_node=parent_node, node_name=node_name )
            parent_node = node_name

def create_path_node(tx, path):
    tx.run( "MERGE (n:path{name:$path})", path=path)

def add_homedir_relation(tx):
    tx.run( "MATCH (a:account),(b:path) WHERE a.homedir = b.name MERGE (a)-[r:homedir]->(b)" )

def add_virtualpath_relation(tx):
    tx.run( "MATCH (a:account),(b:path) WHERE b.name in a.virtualpath MERGE (a)-[r:virtualpath]->(b)" )

def get_virtualpath_list(vpaths):
    start_sep='PhysicalPath,'
    end_sep=',VirtualPath'
    result=[]
    tmp=vpaths.split(start_sep)
    for par in tmp:
        if end_sep in par:
            result.append(par.split(end_sep)[0])
    return result

with open('AccountsDump.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        accountname = row["LoginID"]
        homedir = row["HomeDir"]
        virtualpaths = row["VirtualPath"] if row["VirtualPath"] else 0
        virtualpath_list = get_virtualpath_list(virtualpaths) if virtualpaths else 0
        with driver.session() as session:
            session.write_transaction(process_account_data, accountname, homedir, virtualpath_list)
        line_count += 1
    print(f'Processed {line_count} lines.')

with driver.session() as session:
    session.write_transaction(add_homedir_relation)
    session.write_transaction(add_virtualpath_relation)

