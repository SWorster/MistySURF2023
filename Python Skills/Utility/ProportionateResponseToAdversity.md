# A Proportionate Response To Adversity
## Or: How To Stop Worrying And Love The OS Module

##### Skye Weaver Worster '25J

Having trouble getting your asynchronous code to behave? Is one of Misty's infallible systems inoperable for no apparent reason? Are you stuck in an infinite loop of depression and self-loathing?

Fear not – here is the solution to all that ails you! Introducing the brand-new `reset.py`, for all your debugging needs!

#### Sounds great! But what does it do, exactly?

This code stops, resets, cancels, and unregisters absolutely everything. If your program doesn't end gracefully and leaves some of Misty's processes and events running, this code will stop those for you. It's a great tool for debugging if you want to start with the same preconditions every time.

Some services, such as SLAM and camera services, are usually running by default. As a convenience, `reset.py` will enable these after resetting everything.

#### Wow, that's amazing! Can I really use it for everything?

However, it's not exactly good practice to use a sledgehammer when a screwdriver will do. Use this program sparingly during development. It should never be part of your finished product. This is just a quick and dirty solution what can sometimes be a complicated problem. I would strongly encourage alternate methods of resetting Misty, like unregistering from events and stopping processes in your code, using the reset option in the Settings tab of Misty Studio, or simply turning Misty off and on again.

This program should only be used to quickly transition out of a program that isn't stopping properly. It should never be part of your finished product, and should be avoided during the final phases of testing.

**There are risks to using this program.** Other resetting options, like Misty Studio and turning Misty off, have their own methods of gracefully returning Misty to her default state. Nothing about `reset.py` is graceful. The "blank slate" that you hope this program will create might not be the same preconditions you're expecting. Here's my preferred method of damage control when things go sideways:

1. Type "Control-x Control-c" in your program's terminal. This will end your Python program, but it won't stop whatever commands you've already sent to Misty.
2. Run `reset.py` to immediately stop everything Misty's doing.
3. Misty Studio might take some time to load, so save this for last. Go to the Settings tab and hit the Reset button.

Of course, if Misty is doing something dangerous to herself or others, ignore all of this and simply switch her off.

#### I understand the risks. How can I use this?

You can simply pull up the program in your IDE and hit run. There's nothing to stop you from running two programs at a time, so you could even run this before stopping your original code. However, this might create a new terminal. Be sure to stop your code from the corresponding terminal.

You can also call this program within your code as follows:

```python
import os
os.system('python3 <path-to-file>/reset.py')
```

##### PS: Don't take any of this too seriously. I'm having fun.

##### PPS: But seriously, please be careful when using this code.

##### PPPS: [Don't understand the reference?](https://en.wikipedia.org/wiki/Dr._Strangelove)