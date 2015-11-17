package com.example.alexanderbolinsky.ble_uart_remote;

import android.content.Context;
import android.util.Log;
import android.webkit.JavascriptInterface;
import android.widget.Toast;

/**
 * Created by alexanderbolinsky on 11/16/15.
 */
public class WebAppInterface {
    Context mContext;

    /** Instantiate the interface and set the context */
    WebAppInterface(Context c) { mContext = c; }

    /** Show a toast from the web page */
    @JavascriptInterface
    public void showToast(String toast) {
        Toast.makeText(mContext, toast, Toast.LENGTH_LONG).show();
        Log.e("TAG", "WOAHHHHHH IT WORKS");
    }
}
