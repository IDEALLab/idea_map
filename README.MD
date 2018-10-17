# Interpreting Idea Maps

Code for generating idea maps and calculating novelty scores for sketches. If you use the dataset or the code, please cite "Ahmed, F., Ramachandran, S.K., Fuge, M., Hunter, S. & Miller, S. (2018).  Interpreting Idea Maps: Pairwise comparisons reveal what makes ideas novel. Journal of Mechanical Design".

## Required packages

- numpy
- matplotlib
- scipy
- PIL

## Usage

Run 

```bash
python idea_maps.py
```


## Example: Design Sketches

### Dataset

Our dataset comes from [Milk Frother Design sketches](https://sites.psu.edu/creativitymetrics/).

![Alt text](/sketches/0.jpg)


### Results

2D idea map:

Slice 1:

![Alt text](/output/s_0.png)

### Use your own dataset
Replace images inside sketches folder with your own dataset. Images are named as 0.jpg, 1.jpg and so on.

Replace input.txt with your file containing triplet responses with N rows and 3 columns where N is the number of triplet queries.

A sample row entry "7, 0, 8" in input.txt implies Sketch 7 is more similar to Sketch 0 than Sketch 8.




