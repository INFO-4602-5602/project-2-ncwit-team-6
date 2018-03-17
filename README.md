# Team 6:
- Josiah Buxton
- Brian Lubars
- Kenneth (Hunter) Wapman
- Christopher (Keith) Godley

# How to run it:
- Start up an http server (python or otherwise) and open up the index page at the root of the directory. You can navigate to the visualizations from there!

# visualization 1 (Josiah):
This visualization depicts the male/female ratio of the student population
across all the institutions in the NCWIT dataset.  Because this dataset only
encompasses computing and engineering majors, we expected to see a disproportionate
amount of male to female students.  Each of the spheres in the center of the
screen represents a particular institution in the dataset.  They are dispersed
randomly throughout a 3 dimensional cube.  The size of each sphere corresponds
to the amount of students at that institution (enrollments + freshmen +
sophomores + juniors + seniors + 5th year seniors).  The color of the spheres
can be one of three different cases that are explained in more detail in the
"How to Use" section.

How to Use:

The screen will appear with all of the institutions from the NCWIT Dataset
represented by different spheres.  The camera will constantly spin around
all of the spheres and the user has options available to him/her in the
upper left hand corner of the screen.  He/she can change the data being
displayed with the "Dataset" select option box.  If he/she selects the
data in time slices, another select option box will appear to select a
particular from which data will be shown.  The color select option box changes
the color of the spheres.  The color type select option box allows the user
to view two distinct colors for each sphere representing the male to female
ratio.  The second option allows for one single color to be used to paint
each sphere and the color is determined by a mixture of percentages for
male/female students at an institution.  Because this normally causes the
spheres to appear very similar in color because of the similar M/F ratios,
I implemented another feature that normalizes the color percentages so the
user can gauge differences in the relative M/F ratios for the institutions
in the dataset.

When you hover over each of the spheres, a section of the sphere is highlighted
which pertains to the ratio of male or female students.  If you click on a
sphere, relevant information will be displayed in the lower right hand corner
of the screen.  This includes the institution number, the total number of
students and the male to female ratio of students.

If you'd like to add different data, you can run the parse_data.py script in
the directory with a different input file.  It should output data used by
javascript into the correct format and directory.  

Design Process:

I initially did a lot of sketching to determine how I wanted to view the data.
I knew that I wanted to do view the disparity between male and female students
at each institution. When I was looking through the different vis environments
that I could develop in, I picked WebGL because I thought it would be a great
skill to have in the future.  I began by cleaning the data and getting it into
a json format partitioned by gender.  After I did this, I input this data into
memory through javascript and manipulate it/use it to generate the
visualization displayed by calling different webgl/Three.js functions.  This
took a little bit of time but most of the time was spent refining the vis and
adding new functionality without breaking previously built functions.

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

# visualization (Chris):

For our additional visualization, I decided to keep it simple and display the 
ratio of Asian students for each type of degree at all schools. There are 3 plots 
actually, one showing the ratio of female students, one for male students, and 
one for total students. The specific metrics on display here reflect the asian
student population. 

Design Process:

The idea of these figures is to provide quick, intuitive insight into the Asian
student populous. The viewer can easily see the distribution among each 
demographic in a convenient and familiar pie chart. Labels are turned off by 
default as a design choice so as to allow the user to peak their interest and 
mouse over for interactive information. The type of degree that each slice
represents is provided by a mouseover event, and dissapears when you mouse 
away. The pie charts are a good way to view a static picture of this data.

Thinking of ways to analyze this data interactively was my main focus in designing
these visualizations. I spent more time engaging with the cleaning process, as I
knew this would provide me the flexibility of generating answers to any questions
I could come up with. I developed a scrubber script that took headers as arguments 
and that acted to sort the desired data into the three datasets for the female,
male, and total student demographics. In experimenting with this, I generated some
interesting pie charts that I ended up keeping for the final visualization. In the 
future, this would be a great backend to generate user-specified pie charts, with
an interactive web client as the front end. I used Python to scrub the data and 
output it to the required CSVs, but I then used D3 and Javascript to generate
the visualizations and display them on an HTML page. 
