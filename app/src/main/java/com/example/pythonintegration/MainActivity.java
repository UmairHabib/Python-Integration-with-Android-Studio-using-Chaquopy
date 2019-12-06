package com.example.pythonintegration;

import androidx.appcompat.app.AppCompatActivity;

import android.content.res.AssetManager;
import android.os.Bundle;
import android.widget.TextView;


import com.chaquo.python.PyObject;
import com.chaquo.python.Python;
import com.chaquo.python.android.AndroidPlatform;

import java.io.IOException;
import java.io.InputStream;


public class MainActivity extends AppCompatActivity {


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        try {

            String jsonStr=jsonReader("tmdb_5000_credits.json");
            String jsonStr2=jsonReader("tmdb_5000_movies.json");
            if (!Python.isStarted())
                Python.start(new AndroidPlatform(this));

            Python py= Python.getInstance();
            PyObject pyf = py.getModule("filename");

            PyObject obj= pyf.callAttr("function",jsonStr,jsonStr2);
            TextView textView= findViewById(R.id.text);
            textView.setText(obj.toString());
            System.out.println(obj.toString());

        } catch (IOException e) {
            e.printStackTrace();
        }


    }

    public String jsonReader(String filename) throws IOException {


        AssetManager assetManager=getAssets();
        InputStream input =assetManager.open(filename);
        int size=input.available();
        byte[] buffer=new byte[size];
        input.read(buffer);
        input.close();
        String jsonStr= new String(buffer);
        System.out.println(jsonStr);
        return jsonStr;

    }
}
