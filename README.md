# Payroll Management
## Goal
Provide a simple way to calculate weekly hours and payrate for an employee (including overtime logic), given a number of hours worked each day.
Tool allows to distinguish several pay rates, depending on the type of service provided (e.g. 1 child vs 2 children care).
default values can be modified to avoid re-entering details every time.

## How to Install
`conda create -n payroll pip ipywidgets`  
`pip install -e .`
## Running the GUI
`python main.py --config {yml config file}`

Launches a simple user interface allowing to:
* populate the number of hours executed each day of the week by the service provider for each type of service.
* calculate total hours (broken down by type and overtime)
* record payperiod activity into a csv (TO DO)
It can then calculate hours and paycheck (before taxes) by service type, baking in overtime. 

## Personalizing the services types and rates
cf. `config/example.yml` for an example of config file setup.
you can define there a set of service types, from different providers, with different hourly rates.

## Testing
install package with test suite:  
`pip install -e .[dev]`
running the test suite:  
`pytest --cov=src/ tests/`
 
## GUI Example
![GUI example](images/gui_example.png)

## Learnings
Trying to apply in here some of the principles read from Uncle Bob's Clean Code:
*Martin, Robert C. Clean Code: A Handbook of Agile Software Craftsmanship., Addison-Wesly, 2009*

## To Do
- [x] extract service types into config file
- [ ] extract overtime threshold into config file
- [ ] create drop down list instead of free form text entry for provider definition
- [ ] implement recording functionality to record services provided during a payperiod into a csv file