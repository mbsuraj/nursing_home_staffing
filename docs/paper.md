## Building Early Warning Systems for Nursing Home Workforce Instability

### Abstract

Nursing home staffing shortfalls are well documented — 99 percent of facilities report open positions and high turnover is linked to measurable declines in care quality. At present, workforce monitoring remains largely reactive, identifying shortages only after they emerge rather than anticipating workforce losses before they disrupt care delivery. Using Centers for Medicare and Medicaid Services (CMS) Payroll-Based Journal data covering approximately one million nursing home employees across 51 states from October 2022 through March 2025, we measured monthly employee turnover rates by state, ownership type, and nursing role. We found that turnover follows consistent, structured patterns: monthly rates range from 4 to 13 percent across states, for-profit facilities run 40 percent higher than government-operated ones, and predictable spikes occur in quarter-end months. We then tested whether these patterns could be forecasted, and found that a hierarchical model produced state-level predictions three to six months ahead that reliably identified high-risk states. These findings demonstrate that routinely collected CMS data can support early warning systems for nursing home workforce instability — a capability that grows more important amid evolving federal staffing requirements and increasing state-level responsibility for workforce planning.

### Introduction

The U.S. nursing home sector faces persistent and well-documented workforce instability. Approximately 1.2 million workers deliver direct care to roughly 1.3 million residents across more than 15,000 facilities,¹ yet 99 percent of nursing homes currently report open positions² and turnover among certified nurse aides and licensed nursing staff routinely exceeds 50 percent annually at the facility level.³ Within-facility increases in turnover are associated with measurable declines in care quality, including more health inspection citations and worse outcomes for residents.⁴ As the population aged 75 and older grows through 2035, the consequences of unstable nursing home staffing will compound — for residents, for families, and for state Medicaid programs that finance most long-term care.⁵

Workforce monitoring in nursing homes, however, remains largely descriptive rather than anticipatory. State workforce boards, Medicaid agencies, and facility operators learn about shortages through unfilled shifts, agency reliance, or quality declines — meaning shortages are recognized after they emerge. Recent changes to federal staffing requirements have increased reliance on state and facility-level workforce planning,⁶ making the gap between observation and anticipation more consequential.

To our knowledge, two studies have used CMS Payroll-Based Journal data to characterize nursing home turnover at national scale — documenting its magnitude across facilities³ and its association with care quality.⁴ These studies provide important cross-sectional evidence on the scope of workforce instability. Separately, the Health Resources and Services Administration's Health Workforce Simulation Model projects long-term national supply of nursing personnel through 2038 using survey-based attrition assumptions.⁷ Existing studies do not examine whether turnover follows state-level patterns that could be anticipated in advance, while federal workforce projections are designed primarily for long-term supply planning rather than near-term staffing surveillance.

We examined whether routinely collected federal payroll data contains sufficient structure to support anticipatory workforce planning at the state level. Specifically, we asked whether monthly turnover follows patterns across states, ownership types, and nursing roles that can be anticipated several months in advance.

### Study Data And Methods

#### Data

We used CMS Payroll-Based Journal employee-detail files, which contain daily staffing records for every Medicare- and Medicaid-certified nursing home. Records identify facilities, employee job codes, employment status, and hours worked. Quarterly files from October 2022 through December 2025 covered approximately 15,000 facilities and one million employee records per quarter across 51 states and territories. Data files extended through December 2025; months after the training period were used to validate forecasts and to confirm that identified separations were genuine (the 90-day confirmation window requires subsequent months of observation).

Payroll records were linked to CMS Nursing Home Provider Information files to classify facility ownership as for-profit, non-profit, or government-operated. We restricted analysis to permanent employees in three direct-care nursing roles — registered nurses, licensed practical nurses, and certified nurse aides — excluding contract and agency staff whose transient assignment patterns do not reflect facility workforce instability.

#### Outcome Measure

Our primary outcome was the monthly employee separation rate: the proportion of active employees whose last recorded working day occurred in a given month and who subsequently had no hours reported at the same facility for 90 or more consecutive days, consistent with CMS turnover definitions.⁸ Separation rates were aggregated monthly by state, ownership type, and nursing role.

#### Forecasting Approach

We examined whether turnover patterns could be anticipated using a hierarchical forecasting model that pooled information across states while allowing turnover levels and seasonal patterns to differ by state, ownership, and role. The model was trained on 30 months of historical data (October 2022 through March 2025) and evaluated on subsequent months not observed during training. Forecast performance was assessed using workforce-weighted prediction error, and the model generated state-level forecasts up to six months ahead.

### Study Results

#### Workforce Instability Is Patterned, Not Random

Across the 30-month study period, the national monthly employee separation rate averaged 8.2 percent — equivalent to approximately 64 percent annualized turnover. This rate was not uniform. It varied systematically along three dimensions.

**Geographic variation.** Average monthly separation rates ranged from under 5 percent in Hawaii, New York, and the District of Columbia to above 10 percent in Missouri, Oklahoma, Ohio, Texas, and Kansas (Exhibit 2). This threefold spread across states persisted throughout the study period.

**Ownership gradient.** For-profit facilities — which account for approximately three-quarters of the nursing home sector — experienced monthly separation rates of 8.8 percent, compared with 6.4 percent in non-profit and 6.3 percent in government-operated facilities (Exhibit 3).

**Quarterly periodicity.** Separation rates spiked in quarter-end months (March, June, September, December), averaging 9.3 percent compared with 7.6 percent in other months — a consistent uplift of approximately 1.6 percentage points every third month (Exhibit 1). This pattern appeared across all states and ownership types.

**Role differences.** Certified nurse aides experienced the highest monthly turnover (8.6 percent), followed by licensed practical nurses (7.6 percent) and registered nurses (7.2 percent).

Together, these findings indicate that nursing home turnover follows systematic patterns rather than idiosyncratic fluctuations — creating the conditions necessary for anticipatory workforce monitoring.

#### These Patterns Are Sufficiently Stable to Support Anticipation

Because turnover exhibited structured patterns across states, ownership types, and calendar months, we tested whether these patterns were stable enough to forecast. A hierarchical model trained through March 2025 produced predictions for April through June 2025 — months the model had not previously observed.

The model achieved forecast performance sufficient to distinguish states with persistently elevated turnover from those with more stable workforces, with prediction errors averaging approximately one percentage point among the largest workforce groups (Exhibit 4).

At the national level, the model anticipated the June 2025 quarter-end spike — forecasting a monthly rate of 8.8 percent against an observed 8.9 percent — demonstrating lead time that could support more proactive workforce planning.

### Discussion

These findings suggest that nursing home workforce instability, while severe, is not unpredictable. Monthly separation rates follow stable geographic, ownership, and seasonal patterns — patterns structured enough that a forecasting model trained on routinely collected federal data can identify high-risk states several months before losses materialize. These findings have practical implications for how states and facilities approach workforce planning.

#### Policy and Planning Implications

Currently, workforce interventions in nursing homes — recruitment campaigns, training cohort sizing, agency contracting — are triggered by observed shortages. The patterns documented here suggest an alternative: state workforce boards could use forecasted separation rates to position resources ahead of predictable loss periods. Quarter-end months, which consistently produce elevated turnover across all states, represent foreseeable surges that could help calibrate recruitment timelines in advance. States with persistently high baseline rates — Missouri, Oklahoma, Ohio, Texas, and Kansas exceeded 10 percent monthly throughout the study period — could be prioritized for sustained workforce investment rather than episodic emergency responses.

The ownership gradient carries policy implications as well. For-profit facilities, which dominate the sector, consistently showed separation rates 40 percent above those in government-operated facilities. As Medicaid rate-setting and quality oversight increasingly reference staffing stability, these differential patterns may be relevant to state discussions of retention policy and workforce-linked reimbursement.

#### Relationship to Existing Tools

This work complements rather than replaces existing workforce monitoring. CMS Five-Star ratings and PBJ-based staffing reports provide essential retrospective oversight — confirming whether facilities maintained adequate staffing in prior periods. The Health Workforce Simulation Model offers valuable long-horizon visibility into national supply trajectories. What has been missing is the intermediate layer: state-level, near-term anticipation of workforce losses that could inform quarterly operational decisions. The approach demonstrated here fills that layer using data that is already routinely collected and publicly available.

#### Limitations

Several limitations should be noted. First, our data span 30 months — sufficient to identify seasonal and geographic patterns but too short to detect longer-term structural shifts such as those that might follow major policy changes. Second, the PBJ employee identifier is facility-specific; we cannot distinguish employees who leave the profession entirely from those who transfer to another nursing home or healthcare setting. Our separation rate therefore captures all departures and may overstate true workforce exit. Third, confirmed separation data become available only with a lag, because a departure is confirmed after 90 days without reported hours and payroll files are released quarterly; in practice, these forecasts therefore estimate near-term conditions that are not yet directly observable. Fourth, while the model performed well for large workforce groups, forecasts for small states or rare ownership-role combinations carry wider uncertainty. Finally, demonstrating that turnover can be forecasted is not the same as demonstrating that forecasts change behavior — whether anticipatory information actually improves workforce outcomes remains an implementation question.

#### Future Directions

Operationalizing anticipatory workforce monitoring would require sustained investment in data infrastructure, model maintenance, and integration with state planning processes. As CMS publishes additional quarterly PBJ files, forecast models can be updated and validated over longer horizons. If linked to state-level data on training program enrollment, Medicaid reimbursement, and retention interventions, the forecasts developed here could eventually support integrated workforce planning — where anticipated losses inform specific interventions whose effectiveness can subsequently be measured.

---

### Endnotes

1. National Academies of Sciences, Engineering, and Medicine. *The National Imperative to Improve Nursing Home Quality: Honoring Our Commitment to Residents, Families, and Staff*. Washington, DC: The National Academies Press; 2022.

2. American Health Care Association / National Center for Assisted Living. *State of the Long Term Care Industry: Survey of Nursing Home and Assisted Living Providers*. Washington, DC: AHCA/NCAL; 2024.

3. Gandhi A, Yu H, Grabowski DC. High Nursing Staff Turnover In Nursing Homes Offers Important Quality Information. *Health Aff (Millwood)*. 2021;40(3):384–391.

4. Shen K, McGarry BE, Gandhi AD. Health Care Staff Turnover and Quality of Care at Nursing Homes. *JAMA Intern Med*. 2023;183(11):1247–1254.

5. U.S. Census Bureau. *2023 National Population Projections*. Washington, DC: U.S. Department of Commerce; 2023.

6. Centers for Medicare & Medicaid Services. Medicare and Medicaid Programs; Repeal of Minimum Staffing Standards for Long-Term Care Facilities and Medicaid Institutional Payment Transparency Reporting. *Fed Regist*. 2025;90(231):76521–76534.

7. Health Resources and Services Administration, Bureau of Health Workforce. *Health Workforce Simulation Model: Technical Documentation*. Rockville, MD: HRSA; 2025.

8. Centers for Medicare & Medicaid Services. *Staffing Data Submission Payroll Based Journal (PBJ): Long-Term Care Facility Policy Manual*. Baltimore, MD: CMS; 2024.
