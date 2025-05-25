# ICC-IEEE
Resilient Smart Grid Management through Weather-Informed and Economic Dispatch

ClimaGrid: Resilient and Market-Aware Smart Grid Optimisation

ClimaGrid is an adaptive energy management framework designed to coordinate distributed energy resources (DERs)—including solar, wind, battery, and hydrogen systems—under real-world conditions of weather uncertainty and electricity market volatility.

This repository contains the Python scripts, figures, and simulation assets used in the associated research paper.

🛠 Features

Adaptive Priority-Aware Dispatch (APAD): Balances battery and fuel cell dispatch to smooth demand.

Weather-Responsive Control: Simulates and responds to sudden irradiance and wind fluctuations.

Market-Aware Optimisation: Adjusts DER usage in real-time to reduce cost during high price intervals.

Multi-layer Decision Framework: Integrates technical, environmental, and economic signals.

📂 Repository Structure

graphql

Copy

Edit

📁 ICC_Conference/
├── data_for_energyy.csv          # Rye microgrid dataset (Trondheim, Norway)
├── section_5_1_apad.py           # Load optimisation via APAD
├── section_5_2_resilience.py     # Weather-driven DER response simulation
├── section_5_3_market.py         # Market-aware DER dispatch logic
├── figures/                      # Output figures for the paper
│   ├── figure_3a_climagrid_cloudburst.png
│   ├── figure_3b_climagrid_wind_drop.png
│   ├── figure_4_climagrid_recovery.png
│   └── ...
├── results/                      # LaTeX tables and logs
└── README.md
📈 Dataset Information
This work uses a publicly available dataset from the Rye Microgrid in Langørgen, Trondheim. The data includes:

PV and wind power generation

Local consumption

Historical weather forecasts

Spot market prices

Citation:
P. Aaslid, "Rye microgrid load and generation data, and meteorological forecasts," dataset, 2021.
DOI: 10.5281/zenodo.4448894

▶️ How to Run
Clone this repository:

bash
Copy
Edit
git clone https://github.com/yourusername/climagrid.git
cd climagrid
Install required Python packages:

bash
Copy
Edit
pip install pandas numpy matplotlib seaborn
Run analysis scripts:

bash
Copy
Edit
python section_5_1_apad.py
python section_5_2_resilience.py
python section_5_3_market.py
Output figures will be saved in the figures/ directory.

📊 Figures Generated
Load profile before and after APAD

DER and fuel cell activity under weather stress

Spot market price vs DER dispatch timeline

Grid import vs DER contribution stackplot
