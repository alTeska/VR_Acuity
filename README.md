# Acuity Testing in VR

This research project was coducted at  LMU [Lab of Prof. Sirota](https://www.mcn.uni-muenchen.de/members/regular/sirota/index.html). Project was conducted with data recorded thanks to [ratCAVE project](https://github.com/ratcave)

#### Project Status: [Completed]


## Project Objective

The project was based on experimental data aiming to test the acuity of rodents in ratCAVE environment. During the project I build datasets, analyzed and visualized the data. The main goal of the project consisted of detection of stimuli related behavior in recorded animals. 8 experiments were recorded and used in this analysis. According to German Law, dataset can not be uploaded on github.

### Technologies
* Python
* Pandas, jupyter, datashader
* HDF5
* [ratCAVE](https://github.com/ratcave)

## Project Description
Project aimed at development of basic pipeline required to prove different behaviour exhibited by the animals during the experiment. Animals were presented with a check-board moving in 2 horizontal direction with 3 different speeds.

In the analysis we wanted to prove the stimuli related behaviour (following of the presented pattern) by analysis of angular velocity of the animals. Additionally, I had to take into account the head retraction. The automatic detection of the movement analysis was initiated during last days of the project and it's parts can be found in the provided noteboooks. The implemented pipeline can be found in the scripts. That automatically build the required datasets and calculates all the required values.

The project additionally consisted of paper review and simulation of future experiments. The suggested solutions for ratCAVE have been implemented in separate repository for [Acuity Experiment](https://github.com/alTeska/AcuityExperiment).

## Featured Notebooks
Featured notebooks can be found in report folder.
* [reports/FilterDatabase.ipynb](https://github.com/alTeska/VR_Acuity/blob/master/reports/FilterDatabase.ipynb)
* [reports/PipelineVisualization.ipynb](https://github.com/alTeska/VR_Acuity/blob/master/reports/PipelineVisualization.ipynb)
* [reports/VisualDatabase.ipynb](https://github.com/alTeska/VR_Acuity/blob/master/reports/VisualDatabase.ipynb)


## Acknowledgments
* [Nicholas A. Del Grosso](https://github.com/nickdelgrosso) - for his supervision
* [ratCAVE project](https://github.com/ratcave) - for making the research possible
* Prof. Sirota Lab

## Results

<figure><center>
    <img src="/img/ori_pos.png" width="50%">
<figcaption>
  Visualization of one of the experiments, illustrating the position of the rat (point on the plot) and angle of the animals head with color coding.
</figcaption>
</figure>

<figure><center>
    <img src="/img/SRB.png" width="80%">
<figcaption>
Histograms of stimuli related behavior for different velocities and directions.
</figcaption>
</figure>
