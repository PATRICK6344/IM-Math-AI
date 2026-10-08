package com.im.mathai;

public class ChatMessage {
    public static final int SENDER_USER = 1;
    public static final int SENDER_AI = 2;

    private final String text;
    private final int sender;

    public ChatMessage(String text, int sender) {
        this.text = text;
        this.sender = sender;
    }

    public String getText() {
        return text;
    }

    public int getSender() {
        return sender;
    }
}
