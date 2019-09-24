global data "F:\Shared drives\CADS - Entrepreneurship in Southwest Ohio\Data"
global qcew "F:\Shared drives\CADS - Entrepreneurship in Southwest Ohio\Data\QCEW"

/*-----------------------------------------------------------------------------------------------------*/
/*Import and clean website data*/
/*-----------------------------------------------------------------------------------------------------*/
cd "$data"
import delimited "website_change_panel_v01.csv", clear

gen created_date2 = date(created_date,"MDY", 2019)
gen expired_date2 = date(expired_date,"MDY", 2019)

reshape long changes_in_ , i(url created_date expired_date company_name tag_category category1_id category2_id) j(year)
drop if inlist(year, 2019, 2020)

/*Collapse to levels by year of number of changes and stock of registered sites, new registrations, expired registrations, stock of registered sites with wayback data, new registrations with wayback data, expired registrations with wayback data*/

/*Generate new, exits, and existing indicators for registrations*/
gen new_reg = cond(year(created_date2) == year, 1, 0)
gen exit_reg = cond(year(expired_date2) == year, 1, 0)
gen existing_reg = cond(year(expired_date2) > year & year(created_date2) < year, 1, 0)
rename num_changes tot_changes
rename changes_in num_changes

/*Current data only includes urls that were EVER scraped by the wayback.  Get all urls from Fadel*/
/*Generate new, exits, and existing indicators for registrations that were ever scraped by the wayback machine*/
/*gen new_reg_wayback = cond(year(created_date2) == year, 1, 0)
gen exit_reg_wayback = cond(year(expired_date2) == year, 1, 0)
gen existing_reg_wayback = cond(year(expired_date2) > year & year(created_date2) < year, 1, 0)
*/

/*Collapse to year levels*/
sort year
collapse (sum) new_reg exit_reg existing_reg num_changes, by(year)

/*Generate the stock of registrations*/
gen stock_reg = existing_reg + new_reg - exit_reg

/*Generate year over year changes in levels*/
tsset year
gen d_new_reg = D.new_reg
gen d_exit_reg = D.exit_reg
gen d_existing_reg = D.existing_reg
gen d_num_changes = D.num_changes


sort year
tempfile websitedata
save `websitedata', replace



/*-----------------------------------------------------------------------------------------------------*/
/*Import and clean QCEW data*/
/*-----------------------------------------------------------------------------------------------------*/
cd "$qcew"
use "qcew_data_clean_v01.dta", clear
drop _merge
tsset industry_code year

/*Generate year over year changes in levels*/
gen d_estab = D.annual_avg_estabs_count 
gen d_emp = D.annual_avg_emplvl 
gen d_wages = D.total_annual_wages
gen log_wages = ln(total_annual_wages)
gen d_log_wages = D.log_wages

sort year
tempfile qcewdata
save `qcewdata', replace

/*-----------------------------------------------------------------------------------------------------*/
/* OLS regressions */
/*-----------------------------------------------------------------------------------------------------*/
clear
use `qcewdata'
merge m:1 year using `websitedata'
drop _merge
sort industry_code year
\\\
reg d_estab L.d_estab if industry_code == 10
predict estab1, xb
reg d_estab L.d_estab d_existing_reg if industry_code == 10
predict estab2, xb
reg d_estab L.d_estab d_existing_reg num_changes if industry_code == 10
predict estab3, xb
reg d_estab L.d_estab d_existing_reg d_num_changes if industry_code == 10
predict estab4, xb

twoway (line d_estab year) (line estab1 year) (line estab2 year) (line estab3 year) (line estab4 year) if industry_code == 10, legend(label(1 Actual) label(2 "Model 1") label(3 "Model 2") label(4 "Model 3") label(5 "Model 4")) ylabel(-500 0 500)
cd "$data"
graph export overall_estab.png, replace
\\\


reg d_emp L.d_emp if industry_code == 10
predict emp1, xb
reg d_emp L.d_emp d_existing_reg if industry_code == 10
predict emp2, xb
reg d_emp L.d_emp d_existing_reg num_changes if industry_code == 10
predict emp3, xb
reg d_emp L.d_emp d_existing_reg d_num_changes if industry_code == 10
predict emp4, xb

twoway (line d_emp year) (line emp1 year) (line emp2 year) (line emp3 year) (line emp4 year) if industry_code == 10, legend(label(1 Actual) label(2 "Model 1") label(3 "Model 2") label(4 "Model 3") label(5 "Model 4"))
cd "$data"
graph export overall_emp.png, replace

\\\
reg d_estab L.d_estab if industry_code == 101
predict estab1r, xb
reg d_estab L.d_estab d_existing_reg if industry_code == 101
predict estab2r, xb
reg d_estab L.d_estab d_existing_reg num_changes if industry_code == 101
predict estab3r, xb
reg d_estab L.d_estab d_existing_reg d_num_changes if industry_code == 101
predict estab4r, xb

twoway (line d_estab year) (line estab1r year) (line estab2r year) (line estab3r year) (line estab4r year) if industry_code == 101, legend(label(1 Actual) label(2 "Model 1") label(3 "Model 2") label(4 "Model 3") label(5 "Model 4"))
cd "$data"
graph export relevantind_estab.png, replace

\\\

reg d_emp L.d_emp if industry_code == 101
predict emp1r, xb
reg d_emp L.d_emp d_existing_reg if industry_code == 101
predict emp2r, xb
reg d_emp L.d_emp d_existing_reg num_changes if industry_code == 101
predict emp3r, xb
reg d_emp L.d_emp d_existing_reg d_num_changes if industry_code == 101
predict emp4r, xb

twoway (line d_emp year) (line emp1r year) (line emp2r year) (line emp3r year) (line emp4r year) if industry_code == 101, legend(label(1 Actual) label(2 "Model 1") label(3 "Model 2") label(4 "Model 3") label(5 "Model 4"))
cd "$data"
graph export relevantind_emp.png, replace
