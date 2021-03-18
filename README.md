# assassins_cred
Assasin's CRED project for school

## Prerequsites
* `python >=3.8`
* `pipenv`

## Installation
*  Clone the repository with
```
git clone https://github.com/ScottBot10/assassins_cred.git
```
* cd into the cloned folder
```
cd assassins_cred
```
* Install the packages
```
pipenv install
```
* Rename the default-config.yaml to config.yaml and edit it to suit your purposes
* Setup the input methods (databse, text file, csv file)
* You can now run any of the scripts

## Config
### Special Fetures
  * `!ENV` To use an environment variable (`key: !ENV [ENV_NAME, 'default']` or `key: !ENV ENV_NAME`)
  * `!PATH` Create a path (`key: !PATH ['C:', 'Users']` -> 'C:\Users' or `key: !PATH ['..', '..'] -> /path/to/assassins_cred`)
  * `*PROJECT_ROOT` Alias for the project root (`key: *PROJECT_ROOT` or `key: !PATH [*PROJECT_ROOT, 'resources', 'input_csv.csv']`)
