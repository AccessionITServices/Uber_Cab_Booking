package com.amazonaws.sample.lex;

import android.app.DownloadManager;
import android.os.AsyncTask;
import android.os.Bundle;
import android.app.Fragment;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.Toast;

import android.Manifest;
import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.location.Address;
import android.location.Geocoder;
import android.location.Location;
import android.location.LocationListener;
import android.location.LocationManager;
import android.os.Build;
import android.os.Bundle;
import android.support.v4.app.ActivityCompat;
import android.support.v4.content.ContextCompat;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

//import com.amazonaws.Response;
import com.android.volley.AuthFailureError;
import com.android.volley.NetworkResponse;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.VolleyError;
import com.android.volley.VolleyLog;
import com.android.volley.toolbox.HttpHeaderParser;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONException;
import org.json.JSONObject;

import java.lang.String;
import java.io.UnsupportedEncodingException;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

import static com.android.volley.Response.success;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedInputStream;
import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.UnsupportedEncodingException;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLConnection;

//import static android.support.constraint.Constraints.TAG;

public class web extends Fragment{

    public WebView mWebView;


    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {




        View v=inflater.inflate(R.layout.fragment_, container, false);
        mWebView = (WebView) v.findViewById(R.id.webview);


        RequestQueue requestQueue;
        requestQueue = Volley.newRequestQueue(getActivity ());

        JSONObject jsonBody = new JSONObject();
        try {
            jsonBody.put("name","rahul");
        } catch (JSONException e1) {
            e1.printStackTrace ( );
        }


        final String requestBody = jsonBody.toString();

        StringRequest stringRequest = new StringRequest (Request.Method.POST, "API GATE WAY 2", new com.android.volley.Response.Listener<String> ( ) {
            @Override
            public void onResponse(String response) {

                //mWebView= response;
                mWebView.loadUrl(response.replace ("\"",""));

                // Enable Javascript
                WebSettings webSettings = mWebView.getSettings();
                webSettings.setJavaScriptEnabled(true);

                // Force links and redirects to open in the WebView instead of in a browser
                mWebView.setWebViewClient(new WebViewClient());

            }
        }, new com.android.volley.Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                String errors = (error.toString());
                //Toast.makeText(getApplicationContext(), errors, Toast.LENGTH_SHORT).show();
            }
        }) {
            @Override
            public String getBodyContentType() {
                return "application/json; charset=utf-8";

            }

            @Override
            public byte[] getBody() throws AuthFailureError {
                try {
                    return requestBody==null ? null : requestBody.getBytes("utf-8");
                } catch (  UnsupportedEncodingException uee) {
                    VolleyLog.wtf("Unsupported Encoding while trying to get the bytes of %s using %s", requestBody, "utf-8");
                    return null;
                }
            }

            @Override
            protected com.android.volley.Response<String> parseNetworkResponse(NetworkResponse response) {
                String responseString = "";
                if (response!=null) {
                    try {
                        responseString = new String(response.data, "UTF-8");
                    } catch (UnsupportedEncodingException e) {
                        e.printStackTrace();
                    }

                }

                return success(responseString, HttpHeaderParser.parseCacheHeaders(response));

            }


        };


        requestQueue.add(stringRequest);


        return v;
    }


}
