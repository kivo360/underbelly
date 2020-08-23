# Frustrations With Existing Design Doc

***Losing underbelly specific notes from here on.***

Prior to jumping into the programming the state space any further, it would be wise to start designing the changes that need to be made to fix many of the errors that currerntly exist.

## Problem 1: Parameter Management


The biggest issue with the state space class (and all other classes that require parameters) is the total lack of capacity to manage parameters for each asset. This is absolutely required when managing the observation lag for a given asset. So far, the parameters are stored inside of the individual classes themselves and have no way to share parameters as I'm running a backtest.

I've come to notice this while running a test inside of the reward system. It was a full copy of the `StateEnv`. I noticed that the lookback/lag time was low, and that I needed to change that lag time. i couldn't do it, which was rather frustrating. As I'm writing the underbelly system I'll need to address this. Both with setting the parameters from python, and having those parameters shared asynchronously with the rest of the cluster. 

### Solution: Local Storage + Stream Updates

Inside of `underbelly` I fully intend to create a simple local storage and subscription system that will allow me to push and pull variables to other clients that have subscribed to them. This should be a nice foundation for managing time in the future as well, as there would just be fewer calls in general to be had.


## Problem 2: Decomposiblity

While writing the updates for the reward function I didn't have the means to add new functionality to the system easily. All of the functionality I need are already available, yet everything is entangled. I need to disentangle the code base so there are some highly composable parts that I can transfer elsewhere.


### Solution: SOLID Principles


To make such a setup possible I intend to use the SOLID principles. One in particular is the Dependecy Inversion Principle. It's the act of not depending on details of classes, but on abstractions instead.

For example, a blog article uses user authentication as a valid example.


#### Examples 


```python

class AuthenticationForUser():
  def __init__(self, connector:Connector):
		self.connection = connector.connect()
	
	def authenticate(self, credentials):
		pass
	def is_authenticated(self):
		pass	
	def last_login(self):
		pass

class AnonymousAuth(AuthenticationForUser):
	pass

class GithubAuth(AuthenticationForUser):
	def last_login(self):
		pass

class FacebookAuth(AuthenticationForUser):
	pass

class Permissions()
	def __init__(self, auth: AuthenticationForUser)
		self.auth = auth
		
	def has_permissions():
		pass
		
class IsLoggedInPermissions (Permissions):
	def last_login():
		return auth.last_log

```

For the solution to the problem I have, I could focus on creating generic classes that focuses on the indiviual functionality of the total system. I'm going to use the state space as an example. For the state space I'm doing the following steps in total:


1. Initializing the main variables
    1. In this case I set all of the key elements I'll need to find relavent information to produce the state space. 
        1. The lag time.
        1. The base state space model.
        1. The required or newly named `tag` variables.
        1. The user data access handler.
        1. Optional parameters.
1. Setting properties (`props.py`).
1. Setting highly specific commands (`actions.py`).
    1. You call a lot of the storage commands here. It could be possible to 
1. Getting index data to properly look back on data (`indexing.py`).
1. Getting variables required to create a state space (`contain.py`).
    1. You use "containers", which are essentially dataclasses, to better manage the specifics to the data we're manipulating.
1. Doing online learning to produce the state space (`machine.py`).
    1. 

My new approach would require that I separate the key elements and add the components as a part inside of the `__init__` constructor. This will either look like `PyTorch` or `TensorTrade` if I do it right. For example:

```python
state_env:ComplexEnv = ComplexEnv(
    jamboree=Jamboree()
    scheme=SchemeInterface(), # this would carry entity, submetatype and tag information.
    props=PropsInterface(),
    actions=ActionsInterface(), # This would be where we'd get highly specific information.
    transforms=TransformationInterface(),
    contain=ContainerInterface(),
    storage=StorageInterface() # Here you'd specify the various kinds of storage
)

current_state = state_env.step() # This would get the current state.
```

Either that or a PyTorch inspired design:

```python

class Module:
    def __init__(self, *args, **kwargs):
        self.scheme: Optional[SchemeInterface]= None
        self.time: Optional[TimeInterface]= None
        # Would run stuff here.
    
    def step(self, x, **params):
        self.set_params(**params) # would set schema information to query the data we need.
        return self.forward(x)

class ComplexEnv(jamboree.env.Module):
    def __init__(self, *args, **kwargs):
        super().__init__()
        # This would check for the given fields after the init is called.
        self.essential_fields(
                props=PropsInterface,
                actions=ActionsInterface, 
                transforms=TransformationInterface,
                contain=ContainerInterface,
                storage=StorageInterface,
                parameters=ParametersInterface
            )
        # Jamboree.env.Module will give all modules complete information to all of the essential fields after __init__ is called.
        # Have some way to manage the variables in a 



class StateEnv(ComplexEnv):
    def __init__(self, *args, **kwargs):
        self.scheme=StateScheme()
        self.props=StateProps()
        self.actions=StateActions()
        self.transforms=StateTransformation()
        self.contain=StateContainer()
        self.parameters=StateParameters()
        self.machine=StateMachine() # The internal training loop would go here.
        self.add_schemes(**kwargs) # add schemes if they don't exist.

    def forward(self, x):
        # `x` will be any sort of input we need to access proper information.
        # Some custom arrangement of methods that aren't automated.
        # Have an automated way to take in parameters.
        return self.machine.step()

state_env:StateEnv = StateEnv()
output = state_env.step(input_data, **schema_parameters)

```


## Underbelly Project: Part #1

This is a beautiful design. I love it, I want to use it. Unfortunately it takes hella time. I can't do this in 1 night, even if I wanted to, though it will be a good investment when I'm in the process of revamping the Jamboree library to do everything I need it to. You don't have much time, you need to get something minimal done. It'll be shitty.

So far I need to complete the following things:

1. Order Management
    1. Component Parts
        2. Orders
        3. Broker
    1. Notes:
        1. This could be a good place to test out some new commands.
1. Metrics Monitoring
    1. You need to monitor every variable without using much of any cpu time. You can use the RedisTimeSeries module to make this work and integrate some part into Jamboree's metric handler.
1. Basic Commands
    1. **Delete** -- somehow not doing this properly is coming back to bite you. You need to figure this out. The best option is to create tests around it and debug your way to finishing this part.
        1. I imagine a way to make this work would be to create a handler inside of jamboree's test system then add breakpoints where the variables are being stored and deleted.