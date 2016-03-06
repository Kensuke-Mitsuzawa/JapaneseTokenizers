This document is under 0.6

# How to use

See `/examples/examples.py` to know more about actual usage.

## 1 Initialize object

You initialize `MecabWrapper` object with `mecab_wrapper = MecabWrapper()`.

| argument | type | description | default | options |
|:----------:|:-----------:|:------------:|:------------:|:------------:|
| `dictType` | str | type of dictionary to parse sentences | `ipaddic` | neologd, all, ipaddic, user |
| `path_mecab_config` | str | path to `mecab_config` command works | `/usr/local/bin/` | - |
| `pathUserDictCsv` | str | path to user dictionary csv if you want to use | `` | None |
| osType | str | not used now | - | - |

[Note] `mac` in `osType` might be deprecated some day. This is same as `generic` completly.

## 2 Parse sentence

You can parse sentences with `mecab_wrapper.tokenize(sentence)`

| argument | type | description | default |
|:----------:|:-----------:|:------------:|:------------:|
| return_list | boolean | if True, then list object is return object. Else TokenizedSenetence object. | True |
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


