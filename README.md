# trailing-neo4j

This is a python module to create a graph database to visualise the connection between SFTP accounts and their folders on the servers.

## Pre-requisitues

1. This script takes input from a local csv file called accountlist.csv. A sample of this file is uploaded in this repo.
1. The script also expects the 1st row on the csv file to be as follows:

    | account | homedir | virtualpath |
    | ------- | ------- | ----------- |
    | name  | /path | /path/blah |

1. Install neo4j python package

    ```sh
    $ pip install neo4j
    ```

1. Local version of neo4j database running
1. Login details for neo4j db used in the script _(This will need fixing if you have different username or password)_:<br/>
    Username: `neo4j`<br/>
    Password: `password`

## Running the script

```sh
python sftp_accounts_visualization.py
```
