This document is under 0.3

# How to use

See `/examples/examples.py` to know more about actual usage.

## 1 Initialize object

You initialize `MecabWrapper` object with `mecab_wrapper = MecabWrapper()`.

| argument | type | description | default | options |
|:----------:|:-----------:|:------------:|:------------:|:------------:|
| dictType | str | type of dictionary to parse sentences | `ipaddic` | neologd, all, ipaddic, user |
| osType | str | the os system on which this package works | `generic` | generic, mac, centos |
| pathUserDictCsv | str | path to user dictionary csv if you want to use | `` | None |

[Note] `mac` in `osType` might be deprecated some day. This is same as `generic` completly.

## 2 Parse sentence

You can parse sentences with `mecab_wrapper.tokenize(sentence)`

| argument | type | description | default |
|:----------:|:-----------:|:------------:|:------------:|
| is_feature | boolean | if True, then feature information is in return object | False |
| is_surface | boolean | if True, then __Not-Normalized__ tokens are in return object | False |



### Return object

Return object is set of tokens. Data model is different between `is_feature` True and False.

If `is_feature` is True

```
[
    [
        token,
        [
            pos_big,
            pos_middle,
            pos_small
        ]
    ]
```


If `is_feature` is False


```
[
	token
]
```


