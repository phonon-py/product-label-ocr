```mermaid
graph TD;
    A(App起動)-->B[名前入力];
    B --> C{現品票読込み};
    C --> |OK| D{発注履歴と照合};
    C --> |NG| E[ハンド入力];
    D --> |NG|C;
    D --> A

    

```