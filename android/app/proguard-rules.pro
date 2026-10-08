# Keep line numbers for crash reporting
-keepattributes SourceFile,LineNumberTable
-renamesourcefileattribute SourceFile

# Keep Python runtime
-keep class com.chaquo.python.** { *; }
-keepclassmembers class com.chaquo.python.** { *; }

# Keep our app classes
-keep class com.im.mathai.** { *; }
-keepclassmembers class com.im.mathai.** { *; }

# Keep Android classes
-keep class androidx.** { *; }
-keepclassmembers class androidx.** { *; }

# Remove logging
-assumenosideeffects class android.util.Log {
    public static *** d(...);
    public static *** v(...);
    public static *** i(...);
}

# Optimize
-optimizationpasses 5
-dontusemixedcaseclassnames
