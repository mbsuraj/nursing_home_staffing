## Can Nursing Home Workforce Instability Be Anticipated? Evidence From CMS Payroll Data

### Abstract

Nursing home staffing shortfalls are well documented — 99 percent of facilities report open positions and high turnover is linked to measurable declines in care quality. At present, workforce monitoring remains largely reactive, identifying shortages only after they emerge rather than anticipating workforce losses before they disrupt care delivery. Using Centers for Medicare and Medicaid Services (CMS) Payroll-Based Journal data covering approximately one million nursing home employees across 51 states from October 2022 through March 2025, we measured monthly employee turnover rates by state, ownership type, and nursing role. We found that turnover follows consistent, structured patterns: monthly rates range from 4 to 13 percent across states, for-profit facilities run 25 percent higher than government-operated ones, and predictable spikes occur in quarter-end months. We then tested whether these patterns could be forecasted, and found that a hierarchical model produced state-level predictions three to six months ahead that reliably identified high-risk states. These findings demonstrate that routinely collected CMS data can support early warning systems for nursing home workforce instability — a capability that grows more important amid evolving federal staffing requirements and increasing state-level responsibility for workforce planning.

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

Our primary outcome was the monthly employee separation rate: the proportion of active employees whose last recorded working day occurred in a given month and who subsequently had no hours reported at the same facility for 90 or more consecutive days, consistent with CMS turnover definitions.⁸ We adopted a broader definition of active employment than CMS's regulatory threshold — counting any employee with at least one working day in a given month — because our focus was on anticipating all workforce departures, including those of recently hired staff, rather than regulatory turnover reporting alone. Separation rates were aggregated monthly by state, ownership type, and nursing role.

#### Forecasting Approach

We examined whether turnover patterns could be anticipated using a hierarchical forecasting model that pooled information across states while allowing turnover levels and seasonal patterns to differ by state, ownership, and role. The model was trained on 30 months of historical data (October 2022 through March 2025) and evaluated on subsequent months not observed during training. Forecast performance was assessed using workforce-weighted prediction error, and the model generated state-level forecasts up to six months ahead.

### Study Results

#### Workforce Instability Is Patterned, Not Random

Across the 30-month study period, the national monthly employee separation rate averaged 8.2 percent — equivalent to approximately 64 percent annualized turnover, or nearly one million permanent employee departures per year. This rate was not uniform. It varied systematically along three dimensions.

**Geographic variation.** Average monthly separation rates ranged from under 5 percent in Hawaii, New York, and the District of Columbia to above 10 percent in Missouri, Oklahoma, Ohio, Texas, and Kansas (Exhibit 1). This threefold spread across states persisted throughout the study period and was not driven by a small number of outlier facilities — it reflected broad, state-level differences in workforce stability.

**Ownership gradient.** For-profit facilities — which account for approximately three-quarters of the nursing home sector — experienced annualized turnover of 66 percent, compared with 55 percent in non-profit and 53 percent in government-operated facilities (Exhibit 2). This gradient was consistent across states, suggesting that ownership structure is independently associated with workforce instability.

**Quarterly periodicity.** Separation rates spiked in quarter-end months (March, June, September, December), averaging 9.3 percent compared with 7.6 percent in other months — a consistent uplift of approximately 1.6 percentage points every third month. This pattern appeared across all states, ownership types, and nursing roles, and was the single strongest temporal signal in the data.

**Role differences.** Certified nurse aides experienced the highest monthly turnover (8.6 percent), followed by licensed practical nurses (7.6 percent) and registered nurses (7.2 percent).

Together, these findings indicate that nursing home turnover follows systematic patterns rather than idiosyncratic fluctuations — creating the conditions necessary for anticipatory workforce monitoring.

#### These Patterns Are Sufficiently Stable to Support Anticipation

Because turnover exhibited structured patterns across states, ownership types, and calendar months, we tested whether these patterns were stable enough to forecast. A hierarchical model trained through March 2025 produced predictions for April through June 2025 — months the model had not previously observed.

At the national level, the model closely tracked observed turnover across all three validation months, including the June 2025 quarter-end spike — forecasting 8.8 percent against an observed 8.9 percent (Exhibit 3). The model captured both the level and the quarterly rhythm of national turnover without overfitting to noise.

At the state level, forecast performance was sufficient to distinguish high-instability states from lower-risk ones several months in advance (Exhibit 4). In Missouri, the model forecast monthly rates of 10.6, 11.1, and 12.3 percent for April through June; observed rates were 10.3, 11.5, and 12.3 percent respectively. In Texas, forecasts of 9.2, 9.6, and 11.0 percent aligned with observed values of 9.3, 9.8, and 11.1 percent. In New York — a lower-risk state — the model correctly anticipated rates in the 4.5 to 6.3 percent range, consistent with observations. Across the largest state-ownership-role groups, prediction errors averaged approximately one percentage point.

These results suggest that existing federal payroll data contain sufficient signal to anticipate workforce instability at the state level — not with perfect precision, but with enough accuracy to distinguish where and when losses are likely to be most severe.

### Discussion

These findings suggest that nursing home workforce instability, while severe, is not unpredictable. Monthly separation rates follow stable geographic, ownership, and seasonal patterns — patterns structured enough that a forecasting model trained on routinely collected federal data can identify high-risk states several months before losses materialize. Relative to a seasonal persistence baseline, the hierarchical model reduced prediction error by approximately 25 percent, suggesting that the patterns it captures go beyond simple repetition of prior-year values. Forecasts consistently distinguished high-turnover from low-turnover states across all three validation months. These findings have practical implications for how states and facilities approach workforce planning.

#### Policy and Planning Implications

Currently, workforce interventions in nursing homes — recruitment campaigns, training cohort sizing, agency contracting — are triggered by observed shortages. The patterns documented here suggest an alternative: state workforce boards could use forecasted separation rates to position resources ahead of predictable loss periods. Quarter-end months, which consistently produce elevated turnover across all states, represent foreseeable surges that could help calibrate recruitment timelines in advance. States with persistently high baseline rates — Missouri, Oklahoma, Ohio, Texas, and Kansas exceeded 10 percent monthly throughout the study period — could be prioritized for sustained workforce investment rather than episodic emergency responses.

Concretely, anticipatory forecasts could inform the sizing of CNA training cohorts funded through state Workforce Innovation and Opportunity Act programs, the timing of Medicaid-linked retention bonuses such as those implemented in New York and California,⁹ and the pre-positioning of agency staffing contracts ahead of predicted quarter-end surges.¹⁰ Several states have already implemented workforce incentive programs — the potential contribution of forecasting is to help target these investments where and when they are most needed.

The ownership gradient carries policy implications as well. For-profit facilities, which dominate the sector, consistently showed annualized separation rates approximately 25 percent above those in government-operated facilities. Prior work has linked this gradient to differences in wages, staffing levels, and management practices across ownership types,³ ¹¹ suggesting that Medicaid reimbursement structures and workforce-linked payment incentives may be relevant policy levers.¹² As state oversight increasingly references staffing stability, these differential patterns may inform discussions of retention policy and workforce-linked reimbursement.

State-level variation in turnover likely reflects multiple factors including Medicaid reimbursement generosity, local labor market competition for entry-level workers, and existing state staffing requirements — though disentangling these drivers was beyond the scope of this analysis.¹³

The quarter-end periodicity we observed has not, to our knowledge, been previously documented in the nursing home workforce literature. The pattern may reflect administrative employment cycles such as probationary period endings or quarterly performance reviews, and may also interact with quarterly data reporting processes — though the precise mechanism remains unidentified. Regardless of its cause, the pattern's consistency makes it a useful signal for workforce planning.

#### Relationship to Existing Tools

This work complements rather than replaces existing workforce monitoring. CMS Five-Star ratings and PBJ-based staffing reports provide essential retrospective oversight — confirming whether facilities maintained adequate staffing in prior periods. The Health Workforce Simulation Model offers valuable long-horizon visibility into national supply trajectories. What has been missing is the intermediate layer: state-level, near-term anticipation of workforce losses that could inform quarterly operational decisions. The approach demonstrated here fills that layer using data that is already routinely collected and publicly available.

More broadly, the federal government already invests substantially in nursing workforce development — HRSA allocated over $100 million in nursing workforce grants in 2023 alone.¹⁴ CMS already receives PBJ submissions quarterly and has launched staffing campaign initiatives that include financial incentives for nurses in nursing homes.¹⁵ The infrastructure for an anticipatory monitoring capability therefore already exists; what is missing is the analytic layer that transforms retrospective data into forward-looking workforce intelligence.

#### Limitations

Several limitations should be noted. First, our data span 30 months — sufficient to identify seasonal and geographic patterns but too short to detect longer-term structural shifts such as those that might follow major policy changes. Second, the PBJ employee identifier is facility-specific; we cannot distinguish employees who leave the profession entirely from those who transfer to another nursing home or healthcare setting. Our separation rate therefore captures all departures and may overstate true workforce exit. Third, confirmed separation data become available only with a lag, because a departure is confirmed after 90 days without reported hours and payroll files are released quarterly; in practice, these forecasts therefore estimate near-term conditions that are not yet directly observable. Fourth, while the model performed well for large workforce groups, forecasts for small states or rare ownership-role combinations carry wider uncertainty. Finally, demonstrating that turnover can be forecasted is not the same as demonstrating that forecasts change behavior — whether anticipatory information actually improves workforce outcomes remains an implementation question.

#### Future Directions

Operationalizing anticipatory workforce monitoring would require sustained investment in data infrastructure, model maintenance, and integration with state planning processes. As CMS publishes additional quarterly PBJ files, forecast models can be updated and validated over longer horizons. If linked to state-level data on training program enrollment, Medicaid reimbursement, and retention interventions, the forecasts developed here could eventually support integrated workforce planning — where anticipated losses inform specific interventions whose effectiveness can subsequently be measured. The underlying question this study addresses — whether nursing home workforce instability can be anticipated rather than merely observed — appears, based on this evidence, to have a positive answer.

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

9. New York State Office of the Governor. Governor Hochul Launches Health Care Worker Bonus Program. Albany, NY; 2022. California Department of Health Care Services. Workforce Quality Incentive: Bonus Payments to Skilled Nursing Facilities. Sacramento, CA: DHCS; 2023.

10. Workforce Innovation and Opportunity Act, 29 U.S.C. §3101 et seq. (2014).

11. Sharma H, Xu L. Association Between Wages and Nursing Staff Turnover in Iowa Nursing Homes. *Innov Aging*. 2022;6(4):igac004.

12. Grabowski DC, Feng Z, Hirth R, Rahman M, Mor V. Effect of Nursing Home Ownership on the Quality of Post-Acute Care: An Instrumental Variables Approach. *J Health Econ*. 2013;32(1):12–21. Grabowski DC. Incentivizing Better Quality of Care: The Role of Medicaid and Competition in the Nursing Home Industry. NBER Working Paper No. 24133; 2018.

13. Bhatt CB, Beck AJ. Implementation Challenges of the New Federal Nursing Home Staffing Rules Will Vary Across States. *Health Aff Scholar*. 2025;3(2):qxaf019.

14. U.S. Department of Health and Human Services. Biden-Harris Administration Announces $100 Million to Grow the Nursing Workforce. Washington, DC: HHS; August 10, 2023.

15. Centers for Medicare & Medicaid Services. CMS Nursing Home Staffing Campaign. Baltimore, MD: CMS; 2024.


### Exhibit List

**Exhibit 1.** Average Monthly Employee Separation Rate by State, October 2022–March 2025

SOURCE: Authors' analysis of CMS Payroll-Based Journal employee-detail data.

NOTES: Rates represent the workforce-weighted average monthly proportion of permanent nursing employees (registered nurses, licensed practical nurses, and certified nurse aides) whose last working day at a facility occurred in a given month and who had no subsequent hours reported for 90 or more consecutive days. Alaska and Hawaii are repositioned for display. States not meeting the minimum sample threshold (average monthly active headcount below 30) are shown in gray.

---

**Exhibit 2.** Annualized Employee Separation Rate by Facility Ownership Type, October 2022–March 2025

SOURCE: Authors' analysis of CMS Payroll-Based Journal employee-detail data linked to CMS Nursing Home Provider Information files.

NOTES: Annualized rates computed as 1 − (1 − monthly rate)^12, where monthly rate is the workforce-weighted average separation rate across all states over the full training period. Facility ownership classified as for-profit, non-profit, or government-operated per CMS provider records.

---

**Exhibit 3.** National Monthly Employee Separation Rate: Observed (January 2024–June 2025) and Forecast (April–June 2025)

SOURCE: Authors' analysis of CMS Payroll-Based Journal employee-detail data. Forecasts generated by a hierarchical time-series model trained on October 2022–March 2025 data.

NOTES: "Observed" line represents the national workforce-weighted monthly separation rate for permanent nursing employees. "Forecast" points represent model predictions for months not observed during training. Shaded area denotes the 80 percent prediction interval. Dashed vertical line marks the training cutoff (March 2025).

---

**Exhibit 4.** State Workforce Risk: Forecasted Monthly Turnover Rate vs Nursing Home Workforce Size

SOURCE: Authors' analysis of CMS Payroll-Based Journal employee-detail data. Forecasts generated by a hierarchical time-series model trained on October 2022–March 2025 data.

NOTES: Each point represents one state. The y-axis shows the average forecasted monthly separation rate for April–June 2025. The x-axis shows the total number of active permanent nursing employees in the state as of March 2025 (log scale). Dashed lines represent median values across states. States in the upper-right quadrant (high turnover, large workforce) represent the highest-priority targets for anticipatory workforce planning. Labeled states (OK, MO, OH, TX) are highlighted as exemplars.
