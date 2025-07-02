from psychopy import core, visual

from rewardgym.display.psychopy.primitives import TextStimulusPsychoPy
from rewardgym.tasks.yaml_tools import load_yaml

test_dict = load_yaml("rewardgym/tasks/template/display.yaml")

win = visual.Window(
    size=[1680, 1050],
    fullscr=False,
    color=[-0.5, -0.5, -0.5],
    units="pix",
    checkTiming=True,
    waitBlanking=True,
)

framerate = win.getActualFrameRate()

if framerate is None:
    framerate = 60

episode = test_dict["templates"][test_dict["episodes"][0]["use"]]
stimuli = {
    "fixation": TextStimulusPsychoPy(
        label="fixation", text="+", position=[0, 0], text_color="white"
    ),
    "stim_left": TextStimulusPsychoPy(
        label="stim_left", text="A", position=[-200, 0], text_color="white"
    ),
    "stim_right": TextStimulusPsychoPy(
        label="stim_right", text="B", position=[200, 0], text_color="white"
    ),
}


for k, v in stimuli.items():
    v.setup(window=win)

clock = core.Clock()

trialClock = core.Clock()

print(framerate)
print(episode)

startTime = clock.getTime()

print(startTime, startTime + episode["duration"], clock.getTime())

trialClock.reset()
while (startTime + episode["duration"]) >= clock.getTime():
    t = trialClock.getTime()

    for rend in episode["render"]:
        stimuli[rend["stim"]].draw(
            current_time=t, onset=rend["onset"], duration=rend["duration"]
        )

    win.flip()
    # clock.time += framerate
