# timer
Easy-to-use timer for tracking runtimes. <br><br>
`pip install sometimer`

## Examples
### Main functionality: summary function

```python
from sometimer import timer

# Main functionality is the summary function:
timer.new_checkpoint()
do_stuff()

timer.new_checkpoint(name='useful-name')
do_other_stuff()

...

summary = timer.summary()
print(summary)
```

```
timer summary
              -start-   -duration-
start:         0.000s     0.100s
checkpoint_0:  0.100s     2.305s
useful-name:   2.405s     0.410s
victory lap:   2.815s    12.001s
end:          14.816s
```
<br>

### `timer.__call__()` returns a one-liner
```python
timer()
>>> 'timer:	 0.202s'
```

```python
# and with an active checkpoint:
timer()
>>> 'timer:	 0.303s	    checkpoint_0:  0.050s'
```

<br>

### `@time_this_method` decorator to avoid clutter
Some functions are always heavy (e.g. _load_, _data preprocessing_, _data augmentation_)
and might be useful to time:

```python
from sometimer import time_this_method

@time_this_method
def heavy_preprocessing(data):
    pass
    
@time_this_method(name='more-descriptive-name')
def inefficient_method(data):
    pass
```

when run, yields:

```
heavy_preprocessing(data)
inefficient_method(data)

timer.summary()
>>> 'timer summary
                           -start-   -duration-
start:                      0.000s      0.000s
heavy_preprocessing:        0.000s     25.101s
more-descriptive-name:     25.101s     13.001s
end:                       38.102s'
```

