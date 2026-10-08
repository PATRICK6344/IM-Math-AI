package com.im.mathai;

import android.content.ComponentName;
import android.content.Context;
import android.content.Intent;
import android.content.ServiceConnection;
import android.os.Bundle;
import android.os.IBinder;
import android.view.inputmethod.InputMethodManager;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ProgressBar;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import java.util.ArrayList;
import java.util.List;

public class MainActivity extends AppCompatActivity {

    private IMService imService;
    private boolean bound = false;

    private RecyclerView chatRecyclerView;
    private EditText chatInput;
    private Button sendButton;
    private Button learnBtn, solveBtn, theoryBtn;
    private ProgressBar modelLoadingProgress;

    private final List<ChatMessage> messages = new ArrayList<>();
    private ChatAdapter chatAdapter;

    private final ServiceConnection connection = new ServiceConnection() {
        @Override
        public void onServiceConnected(ComponentName name, IBinder service) {
            IMService.LocalBinder binder = (IMService.LocalBinder) service;
            imService = binder.getService();
            bound = true;
            modelLoadingProgress.setVisibility(ProgressBar.GONE);
            addAiMessage("IM Pro Max ready! 🚀\nUse me to solve equations, learn concepts, or explore new theories.");
        }

        @Override
        public void onServiceDisconnected(ComponentName name) {
            bound = false;
        }
    };

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        chatRecyclerView = findViewById(R.id.chatRecyclerView);
        chatInput = findViewById(R.id.chatInput);
        sendButton = findViewById(R.id.sendButton);
        learnBtn = findViewById(R.id.learnBtn);
        solveBtn = findViewById(R.id.solveBtn);
        theoryBtn = findViewById(R.id.theoryBtn);
        modelLoadingProgress = findViewById(R.id.modelLoadingProgress);

        chatAdapter = new ChatAdapter(messages);
        chatRecyclerView.setLayoutManager(new LinearLayoutManager(this));
        chatRecyclerView.setAdapter(chatAdapter);

        modelLoadingProgress.setVisibility(ProgressBar.VISIBLE);
        addAiMessage("Loading model...");

        Intent intent = new Intent(this, IMService.class);
        bindService(intent, connection, Context.BIND_AUTO_CREATE);
        startService(intent);

        sendButton.setOnClickListener(v -> sendMessage());

        learnBtn.setOnClickListener(v -> {
            String fact = chatInput.getText().toString().trim();
            if (fact.isEmpty()) {
                Toast.makeText(this, "Enter a fact to learn.", Toast.LENGTH_SHORT).show();
                return;
            }

            appendUserMessage(fact);
            chatInput.setText("");
            hideKeyboard();

            new Thread(() -> {
                String response = imService.learnFact(fact);
                runOnUiThread(() -> addAiMessage(response));
            }).start();
        });

        solveBtn.setOnClickListener(v -> {
            String expr = chatInput.getText().toString().trim();
            if (expr.isEmpty()) {
                Toast.makeText(this, "Enter an equation (e.g., x^2 - 5x + 6 = 0).", Toast.LENGTH_SHORT).show();
                return;
            }

            appendUserMessage(expr);
            chatInput.setText("");
            hideKeyboard();

            new Thread(() -> {
                String response = imService.solveEquation(expr);
                runOnUiThread(() -> addAiMessage(response));
            }).start();
        });

        theoryBtn.setOnClickListener(v -> {
            appendUserMessage("Generate a theory...");
            new Thread(() -> {
                String response = imService.generateTheory();
                runOnUiThread(() -> addAiMessage(response));
            }).start();
        });
    }

    private void sendMessage() {
        String message = chatInput.getText().toString().trim();
        if (message.isEmpty()) return;

        appendUserMessage(message);
        chatInput.setText("");
        hideKeyboard();

        new Thread(() -> {
            String response = imService.chatWithAI(message);
            runOnUiThread(() -> addAiMessage(response));
        }).start();
    }

    private void appendUserMessage(String text) {
        messages.add(new ChatMessage(text, ChatMessage.SENDER_USER));
        chatAdapter.notifyItemInserted(messages.size() - 1);
        chatRecyclerView.scrollToPosition(messages.size() - 1);
    }

    private void addAiMessage(String text) {
        messages.add(new ChatMessage(text, ChatMessage.SENDER_AI));
        chatAdapter.notifyItemInserted(messages.size() - 1);
        chatRecyclerView.scrollToPosition(messages.size() - 1);
    }

    private void hideKeyboard() {
        InputMethodManager imm = (InputMethodManager) getSystemService(Context.INPUT_METHOD_SERVICE);
        if (imm != null && getCurrentFocus() != null) {
            imm.hideSoftInputFromWindow(getCurrentFocus().getWindowToken(), 0);
        }
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        if (bound) {
            unbindService(connection);
            bound = false;
        }
    }
}
