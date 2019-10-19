```
; 数字列を数値に変換するプログラム
DTOB START
     RPUSH ; GR1〜7の内容をスタックに退避
     ADDL GR2,GR1 ; 論理加算 GR2 = address(GR1) + GR2 : 数字列の最後尾+1を GR2 に代入
     LAD GR0,0 ; 戻り値の初期化: LD GR0,=0
     ; 数字列を[0]〜[最後尾+1]まで走査
LOOP CPL GR1,GR2 ; GR1 - GR2 => FLAG
     JZE FIN ; FLAG == 0 -jump-> FIN 
     LD GR4,0,GR1; GR4 = GR1[0]: 数字列1文字を GR4 に取り出す
     SUBL GR4,='0'; unsigned GR4 -= '0'(#30=48): GR4 を数値に変換
     ; GR0 を10倍（桁上げ）して GR4 を加算
     SSL GR0,1 ; GR0 = GR0 << 1: GR0 を 2^1倍
     LD GR5,GR0 ; GR5 = GR0
     SLL GR5,2 ; GR5 = GR5 << 2: GR5 を 2^2倍
     ADDL GR0,GR5 ; unsigned GR0 += GR5
     ADDL GR0,GR4 ; unsigned GR0 += GR4
     LAD GR1,1,GR1 ; 先頭アドレスをインクリメント: GR1 = GR1[1]
     JUMP LOOP ; -jump-> LOOP
FIN  RPOP ; GR1〜7の内容をスタックから戻す
     RET ; 呼び出し元に戻る
     END
```

```
; 文字列を数値配列として管理テーブルに格納するプログラム
GETWD START
      RPUSH ; GR1〜7の内容をスタックに退避
      LD GR6,GR1 ; 引数文字列の先頭アドレスをGR6にセット
      LD GR7,GR2 ; 引数管理テーブルの先頭アドレスをGR7にセット
      LD GR3,=-1 ; 数字列の処理状態フラグ: GR3 = -1（未処理）
      LAD GR6,-1,GR6 ; GR6 = address(GR6[-1])
LOOP  LAD GR6,1,GR6 ; ループ開始: ポインタをインクリメント
      LD GR4,0,GR6; GR4にポインタ位置の1文字を取り出す
      ; GR4が'.'ならループ終了
      CPL GR4,='.'
      JZE FIN ; unsigned GR4 - '.' == 0 -jump-> FIN
      ; GR4が' 'ならSETWD を呼び出す
      CPL GR4,=' '
      JNZ NUM ; unsigned GR4 - ' ' != 0 -jump-> NUM
      CALL SETWD
      JUMP LOOP ; ループ継続 
      ; 数字列処理
NUM   LD GR3,GR3 ; GR3 => FLAG
      JZE LOOP ; FLAG == 0 -jump-> LOOP
      ; 数字列処理フラグが立っていない場合
      LD GR3,=0 ; 数字列の処理中フラグを立てる
      LD GR1,GR6 ; 現在処理中の数字列の先頭アドレスをGR1に退避
      JUMP LOOP ; ループ継続 
FIN   CALL SETWD ; 最後の数字列を管理テーブルポインタに格納
      LD GR2,=-1; 管理テーブルの終了位置標識
      ST GR2,0,GR7 ; GR2 => address(GR7[0]): 管理テーブルポインタにGR2格納
      RPOP ; GR1〜7の内容をスタックから戻す
      RET ; 呼び出し元に戻る
      END

; 数字列を数値に変換して管理テーブルポインタに格納するプログラム
SETWD START
      ; 数字列処理フラグが0でないなら終了
      LD GR3,GR3 ; GR3 => FLAG
      JNZ FIN2 ; FLAG != 0 -jump-> FIN2
      ; GR2に現在処理中の数字列の先頭アドレスをセット
      LD GR2,GR6 ; 処理中数字列の 最後尾+1 の位置
      SUBL GR2,GR1; unsigned 最後尾+1 - 先頭 => 数字列の先頭アドレスを 0 に正規化したアドレス
      CALL DTOB ; DTOB を呼び出して数字列を数値に変換
      ST GR0,0,GR7 ; GR0 => address(GR7[0]): 変換結果を管理テーブルポインタに格納
      LD GR3,=-1 ; 数字列処理フラグを-1にする
      LAD GR7,1,GR7 ; 管理テーブルポインタをインクリメント
      RET
      END
```

2進数の乗算は、乗数が0になるまで以下の手順を繰り返せば良い

1. 乗数の最下位ビットが1なら、被乗数の値を乗算結果に加算
2. 被乗数を1ビット左シフト（被乗数を倍にする）
3. 乗数を1ビットを右シフト（乗数を半分にする）

```
; 文字列内の2つの数字列を乗算するプログラム
MULT START
     RPUSH ; GR1〜7の内容をスタックに退避
     LAD GR2,CTBL ; CTBLの先頭アドレスをGR2にセット
     CALL GETWD ; GETWD呼び出し => GR2 = [数値,数値,-1]
     LD GR4,0,GR2 ; 被乗数をGR4にセット
     LD GR5,1,GR2 ; 乗数をGR5にセット
     LD GR0,=0 ; 戻り値を0初期化
     ; GR5が0ならそのまま終了 => 戻り値 = 0
     LD GR5,GR5 ; GR5 => FLAG
     ; GR0 = GR4 * GR5 実行
LOOP JZE FIN ; FLAG == 0 -jump-> FIN
     LD GR3,GR5 ; GR3 = GR5
     AND GR3,=#0001 ; 乗数の最下位ビット == 1?
     JZE NEXT ; 乗数の最下位ビット == 0 -jump-> next
     ADDL GR0,GR4 ; unsigned GR0 += GR4
NEXT SLL GR4,1 ; 被乗数を2倍に
     SRL GR5,1 ; 乗数を半分に
     JUMP LOOP ; GR5 => FLAG -jump-> LOOP
FIN  RPOP ; GR1〜7の内容をスタックから戻す
     RET ; 呼び出し元に戻る
     END

; GETWD用管理テーブル確保
CTBL DS 3
     END
```
