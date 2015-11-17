
---------------------------------------------------------------------------------------------
----- "Heart Rate, Audio, and Video Data in Human-Computer-Interaction Corpus" (HeartAV) ----
---------------------------------------------------------------------------------------------


The data package of "Heart Rate, Audio, and Video Data in Human-Computer-Interaction Corpus" (HeartAV-Corpus) are gathered by the team members of Experimental Industrial Psychology at University of Wuppertal, headed by Prof. Dr. Jarek Krajewski. It contains synchronized Heart Rate, Audio and Video Data from 71 subjects during various Human-Computer-Interaction tasks.





(I) File naming for data files: 

vp_§§§_$$_%% with


§§§: subject ID (3 digits, 035-078; each number represents a different subject ID);the subject ID can be inferred from the metadata excel file "MetaData_HeartAV.xlsx"
$$ : sleep deprivation condition (01= sleep deprivation; 02 = no sleep deprivation)
%% : ID of the actiwatch used to monitor sleep and sleep deprivation





The package of HeartAV contains three subfolders. 

(II) Heart Rate files

The folder HeartAV_HeartRateFiles contains a file HeartRate.xlsx with the original Heart Rate per second (HR) and outlier-corrected Heart Rate per second (HROut) of each participant and a timeline (CET) from beginnig of the session until end of the session. The timeline is corresponding to the logfiles in the folder HeartAV_HCITaskLog of each participant, which includes information about the length and name of the specific tasks during the session.

Assessment of Heart Rate (HR)
HR were assessed with an mobile ECG-belt, measured through two electrodes on the chest. The ECG signal was digitized at 1024 Hz. The calculation of HR per second was based on the time of the R-R intervals.  


(III) Logfiles

The folder HeartAV_HCITaskLog contains .xls files of each participant (e.g. 075_02_00_Log.xls), corresponding to a .ppt presentation, the participant gets to use during a session. Leaving a slide and changing to the next one sets a timestamp in Column F.  
Column A, first value,  refers to Subject ID.
Column B = .ppt slide with task/stimulus or instruction during the session
Column C = Running number of .ppt slide 
Column D = Name of ppt presentation 
Column E = Date of session
Column F = Timestamp of beginning of each task (see Column B)
Column G = Participant's selfrating score referring to parameters in Column B; 

Tasks in Column B:
xx_pre = refers to a slide with preparation for the following audiotask (e.g. rd_butter_pre = preparation about the task reading the "Buttergeschichte", rd_butter)
instructions_xx = refers to a slide with instructions regarding the following task (e.g. instruction_tat = instructions about the task TAT)
start_baseline_ord = start baseline measure (Subject is asked to sit still until end of baseline measure, breathing normally, not speaking)
stop_baseline = end of baseline measure
instruction and wait_for_instructions =  instruction about the experiment 
test = sound test
tat_xx = TAT, Thematic Apperception Test. Telling a story based on a specific tat picture. xx = Type of picture (e.g. tat_cry = telling a story based on a tat picture of a crying person.
KSS_xx = KSS score based on participant's selfrating after a specific task xx. KSS = karolinska Sleepiness Scale. Score from 1 to 10. For score see column G. 
stimulus_xx = picture or video of a stimulus (e.g stimulus_cup = picture of a cup)
instruction_emo = instruction for self rating on emotional state on a visual analogue scale (VAS) after a stimulus. (0-100; 0 = low parameter value 100 = high parameter value) 
emo_disgust = self rating for emotional state "disgust" on VAS after a specific stimulus. For score see column G.
emo_fear = self rating for emotional state "fear" on VAS after a specific stimulus. For score see column G.
emo_sorrow = self rating for emotional state "sorrow" on VAS after a specific stimulus. For score see column G.
emo_amused = self rating for emotional state "amused" on VAS after a specific stimulus. For score see column G.
emo_shame = self rating for emotional state "shame" on VAS after a specific stimulus. For score see column G.
interested = self rating for emotional state "interested" on VAS (0-100; 1 = low parameter value 100 = high parameter value). For score see column G.
satisfied = self rating for emotional state "interested" on VAS (0-100; 1 = low parameter value 100 = high parameter value). For score see column G.
strained = self rating for emotional state "interested" on VAS (0-100; 1 = low parameter value 100 = high parameter value). For score see column G.
sad = self rating for emotional state "interested" on VAS (0-100; 1 = low parameter value 100 = high parameter value). For score see column G.
annoyed = self rating for emotional state "interested" on VAS (0-100; 1 = low parameter value 100 = high parameter value). For score see column G.
happy = self rating for emotional state "interested" on VAS (0-100; 1 = low parameter value 100 = high parameter value). For score see column G.
bored = self rating for emotional state "interested" on VAS (0-100; 1 = low parameter value 100 = high parameter value). For score see column G.
activated = self rating for emotional state "interested" on VAS (0-100; 1 = low parameter value 100 = high parameter value). For score see column G.
stressed = self rating for emotional state "interested" on VAS (0-100; 1 = low parameter value 100 = high parameter value). For score see column G.
uncomfortable = self rating for emotional state "interested" on VAS (0-100; 1 = low parameter value 100 = high parameter value). For score see column G.
start_keylog_ord to end_keylog = HCI task, where participant's keyboard behavior during an office task is logged
office_word = office task, copying a printed text attached to participant's monitor into MS word document.
start_mouselog to KSS_uni_mousetask = HCI task, where participant's mouse behavior during a website task is logged
prepare_for_speech = refers to a slide with preparation for the following reading task
prepare_for_reading_xx = refers to a slide with preparation for the following reading task; xx = name of following task
chin = slide, which announces the use of a chin rest for the participant
end_ord = end of session
star_eyetracking = start eyteracking session (not included in Data Corpus)
 


(III) Audio files

Audio files included in the package of HeartAV :
HeartAV_AudioFiles is a folder with audio files (.wav) of the participants. For file naming see (I).
The files are categorized into folders by the different purposes of phonations.

 The meanings of audio file names in alphabetical order (please see below):

a_comf = phonation of vowel [a] in comfortable intensity
a_power = phonation of vowel [a] in loud intensity
a_sad = phonation of vowel [a] in a sad way
a_smile = phonation of vowel [a] in a glad and joyful way
air_cess = simulated air traffic controller phrase (read speech)
coffee = command phrase (read speech)
counting = counting from 1 to 40
cup = describing the picture of a cup
dry = asking about the weather (read speech)
embassy = asking for directions to the embassy (read speech)
emergency = asking about an emergency case (read speech)
evening = command phrase (read speech)
face = describing the picture of a fatally wounded face
flight = simulated air traffic controller communication (read speech)
fridge = command phrase (read speech)
friesen = asking for directions (read speech)
frontdoor = command phrase (read speech)
gangrene = describing the picture of a necrotic foot
gmx = describing a website
hamburg = asking directions to hamburg (read speech)
hopp = talking about the ragistrar's office hours
juliet = simulated air traffic
laundry = command phrase (read speech)
ocean = ocean survival task, monolog/dialog description
openoffice = describing a task on the computer
pinkflamingo = describing a short movie with a transvestite
present = talking about the greatest gift one got
rd_butter = reading the story "Butter"
rd_faber = reading the story "Homo Faber"
rd_faber2 = reading the story "Homo Faber"
rd_northw = reading the story "North Wind"
rd_rainbow = reading the story "Rainbow"
rd_zeh = reading a newspaper article
reststop = talking about a break at the rest stop (read speech)
roger = simulated air traffic controller phrase (read speech)
sg_cream = singing the song "Sahne"
sg_good_evening = singing the song "Guten Abend"
story_disgust_childhood = talking about a disgusting moment from childhood
story_sad_childhood = talking about a sad moment from childhood
study = determining a paper's author
surgery = describing the video of a surgery
tampons_thermal = describing a picture of a tampon
tat_boat = telling a story based on a tat picture of a boat
tat_boy = telling a story based on a tat picture of a boy
tat_cookie = telling a story based on a tat picture of a cookie
tat_cry = telling a story based on a tat picture of a crying person
tat_ladies = telling a story based on a tat picture of ladies
tat_men = telling a story based on a tat picture of men
tat_nanny = telling a story based on a tat picture of a nanny
toilet = describing a picture of a dirty toilet
traffic = common car traffic phrase (read speech)
tv = command phrase (read speech)
vomit = describing the picture of a person vomiting



(IV) Video files









