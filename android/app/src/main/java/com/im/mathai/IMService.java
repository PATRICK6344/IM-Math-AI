package com.im.mathai;

import android.app.Service;
import android.content.Intent;
import android.os.Binder;
import android.os.IBinder;
import android.util.Log;

import androidx.annotation.Nullable;

import com.chaquo.python.PyObject;
import com.chaquo.python.Python;
import com.chaquo.python.android.AndroidPlatform;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;

import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;

public class IMService extends Service {
    private static final String TAG = "IMService";
    private final IBinder binder = new LocalBinder();
    private Python py;
    private PyObject imAgent;

    public class LocalBinder extends Binder {
        public IMService getService() {
            return IMService.this;
        }
    }

    @Override
    public void onCreate() {
        super.onCreate();

        try {
            if (!Python.isStarted()) {
                Python.start(new AndroidPlatform(this));
            }
            py = Python.getInstance();
            imAgent = py.getModule("im_agent");
            Log.d(TAG, "Python runtime initialized");

            new Thread(this::ensureModelDownloaded).start();

        } catch (Exception e) {
            Log.e(TAG, "Python init failed", e);
        }
    }

    private void ensureModelDownloaded() {
        File modelDir = new File(getFilesDir(), "models");
        if (!modelDir.exists()) {
            modelDir.mkdirs();
        }

        File modelFile = new File(modelDir, "mistral.gguf");

        if (!modelFile.exists()) {
            try {
                downloadModel(modelFile);
            } catch (Exception e) {
                Log.e(TAG, "Download failed", e);
                return;
            }
        }

        try {
            String result = imAgent.callAttr("initialize_llm", modelFile.getAbsolutePath()).toString();
            Log.d(TAG, "LLM init: " + result);
        } catch (Exception e) {
            Log.e(TAG, "LLM init error", e);
        }
    }

    private void downloadModel(File targetFile) throws IOException {
        String url = "https://huggingface.co/TheBloke/Mistral-7B-GGUF/resolve/main/mistral-7b-instruct-v0.2.Q4_K_M.gguf";

        OkHttpClient client = new OkHttpClient();
        Request request = new Request.Builder()
                .url(url)
                .build();

        try (Response response = client.newCall(request).execute()) {
            if (!response.isSuccessful()) {
                throw new IOException("Download failed: " + response.code());
            }

            if (response.body() == null) {
                throw new IOException("Empty response body");
            }

            try (InputStream in = response.body().byteStream();
                 FileOutputStream out = new FileOutputStream(targetFile)) {
                byte[] buffer = new byte[8192];
                int read;
                while ((read = in.read(buffer)) != -1) {
                    out.write(buffer, 0, read);
                }
            }
        }
    }

    public String chatWithAI(String message) {
        try {
            return imAgent.callAttr("chat_with_llm", message).toString();
        } catch (Exception e) {
            Log.e(TAG, "Chat error", e);
            return "Error: " + e.getMessage();
        }
    }

    public String learnFact(String fact) {
        try {
            return imAgent.callAttr("learn", fact).toString();
        } catch (Exception e) {
            return "Error: " + e.getMessage();
        }
    }

    public String solveEquation(String equation) {
        try {
            return imAgent.callAttr("solve", equation).toString();
        } catch (Exception e) {
            return "Error: " + e.getMessage();
        }
    }

    public String generateTheory() {
        try {
            return imAgent.callAttr("generate_theory").toString();
        } catch (Exception e) {
            return "Error: " + e.getMessage();
        }
    }

    @Nullable
    @Override
    public IBinder onBind(Intent intent) {
        return binder;
    }
}
