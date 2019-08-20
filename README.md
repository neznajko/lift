![concept](pix/concept72.png)
## *題 namba tuu*
**I**n this problem there are bunch of lifts, synchronized by an external
clock, controlled by a ***Command Center***, that is the program we have
to write, by receiving *external* and *internal* requests on each clock
tick. The problem of the
[*problem*](https://ioinformatics.org/files/ioi1989problem2.pdf)
is that it only takes the lift's perspective, zo all inputs have to
be done manually (one should take care that there are no internal
requests from an empty lift etc.). Zo I've decided to extend the program
from pure controlling unit to a simulation based on a *scv* requests
in the form ***(orig, dest)***, vich are later transformed into internal
requests.

### ℥ʈrateζy
**Okay** if I was responsible for the lift strategy, there will be a lot
of *scv* complains in the *Com Center* (not to mention that I'm living
on ze second floor). If ve hafe a **marinne** on ze first floor going to
ze last floor, and in the next cycle, a *scv* appears vith a reqvest
***3 ▷ 10***, vat ve are going to zo? Thatz the Q! The Answer
is we pick that *scv*, but that's not always the case, for if we have an
empty lift going up called from a request that's going down or
vice versa we raise an *ignore flag*, otherwise we pick all *scv* requests
from the waiting *queue* with same directions as the lift. ***Thatz.***

### *The algorithm*
The decisions a lift takes are handled by a sequence of *actions*
per *clock cycle*. There are six different *actions*:

1. *wait4req* (waiting for requests)
2. *queueck*  (queue check)
3. *nta*      (enter)
4. **justGou**  (go go go)
5. *exit*     (what is this?)
6. *arvedon*  ***(eNOuPe)***

At the end of each *action* we assign the ***next*** *action*
depending on different conditions, e.g. the *next* ***action***
of *wait4req* is either the same or *queueck* depending if there
is a request etc. Here is the complete action graph:

![action_graph](pix/action_graph.png)

## lift.py
You can view short descriptions and default values of *lift.py*
options with:

```lift.py --help```

The following is a bit more detailed explanation of more obscure options:

* mode 

  if non zero all even and odd request will be assigned to an even
  or odd indexed lifts respectively

* lambda

  from *Probability Theory* we know that the number of people entering
  a building per unit time is a *Poisson Distribution*. The value of
  this parameter is equal to the mean number of *scvs* entering the
  *Com Center* per ***clock cycle***. It is used when *--simula*
  option is set. Usually one has to increase this value when there are
  moar number of lifts.

* visual

  Ze old hacker (xterm control seq). This is a screenshot at the end
  of the following command:
  
  ```lift.py -n 30 --lambda 1.5 --visual --nlifts 2```

  Canvas width per lift is 35, zo for 4 or moar lifts make sure you are
  on a fullscreen.

![Screenshot](pix/Screenshot.png)

https://youtu.be/Qo4JIT8jMtI