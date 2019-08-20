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
ze top, and after that while ze lift is moving, a *scv* appears vith
a reqvest ***3 ▷ 10***, vat ve are going to zo? Thatz the Q!