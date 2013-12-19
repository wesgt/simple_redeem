simple_redeem
=============

simple redeem service

* receive-redeem-code
* redeem-gift

test server : http://54.238.225.130/

## Requirements

* Python 3.3.2
* Flask 0.10
* MySQL / MariaDB
* sqlalchemy
* pymysql3

## RECEIVE_REDEEM_CODE

應用程式可利用此界面用使用者輸入的 email 來取得一個 redeem code.

INPUT

| endpoints           | method    | data        |
| --------            | --------  | --------    |
| /gogolook/redeem_code | post      | email='user@test.com.tw' |

OUTPUT(json)

| parameter   | value     |
| --------    | --------  |
| result      | receive_success, email_fail|
| redeem_code | 八個英數字組合|

## REDEEM_GIFT

應用程式可利用此界面拿使用者輸入的 redeem code 來兌換禮物並回應是否成功

INPUT

| endpoints           | method    | data        |
| --------            | --------  | --------    |
| /gogolook/redeem_gift | post      | email='user@test.com.tw', redeem_code='xxxxxxxx' |

OUTPUT(json)

| parameter   | value     |
| --------    | --------  |
| result      | redeem_gift_success, email_not_receive_redeem_code_fail, redeem_gift_count_greater_than_three_fail, redeem_code_fail, redeem_code_duplicate_fail, redeem_code_is_me_fail|

