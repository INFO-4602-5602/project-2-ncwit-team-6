# Team 6:
- Josiah (SweetCheeks) Buxton
- Brian (Swivelbottom) Lubars
- Kenneth (Hunter) Wapman
- Christopher (Keith) Godley

# How to run it:
- start up a server (python or otherwise) and open up the index page at the root of the directory. you can navigate to the visualizations from here!

# visualization 1 (Josiah):
- grid of circles
    - circle = school
    - two colors in circle
    - colors represent gender
    - interactive:
        - user can control year
        - year will move automatically

# visualization 2 (Hunter):
This visualization shows how the percentage of women in a given major changed over time. 

My design process for this visualization started with the simplest question someone might want to know: how has the percentage of women in STEM majors changed over time? I then thought it would be interesting to split this up by major. However, when I did this, I found that there were too many majors for any really sensical plot to be meaningful, so I limited the set of majors I was looking at to those which had more than 10 years of data, so the user could really see trends.

The visualization is titled "Percentage of Women in different majors over time".

# visualization 3 (Brian):
This visualization tracks student retention for computer science majors at a specific university and class over the course of a 4-year degree program. We can see the number of male and female students, and how they change as a class moves from Freshman to Sophomore to Junior to Senior. For example, We can look at institution 2, and ask ourselves: of the students who started in institution 2 in a CS major in 2009, how many graduated in 2013?

My design process started with the question above: what does student retention rate look like for different institutions and different genders? Is there a difference between Male and Female retention? I originally wanted to split this up further by race, but the data was too sparse to support this. A drop-down lets the user select which institution and class to view the stats for. In the drop-down, the class years are grouped by institution. The institutions are in the same order as the original CSV given to us, but it is filtered, so we're missing over half of the institutions. D3 was used to produce it.

I had to filter to make sure we had enough data to display all 4 years. This eliminated two types of (institution,class) pairs unforunately:
1. Classes which were too recent (class of 2018 or later) are not displayed, because we can't see all 4 years of them.
2. Institutions which don't have 4 years of M/F data broken down by class are not displayed. 

A line graph was chosen with a line per gender, because this is really the clearest way of representing such time-series data. This data is more fine-grained than the other visualizations. The other visualizations provide good high-level views of the gender/race differences, and this visualization provides detail for a single institution and class, so they complement each-other well.

**Interactivity:** A hover tooltip displays the gender, year, and number of students for each point. Selecting a different institution/class from the drop-down will render the data for that combination in place of the previous data. Male is shown in Blue, and Female is shown in Red.

