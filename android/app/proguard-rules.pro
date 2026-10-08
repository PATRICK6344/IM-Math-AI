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
-keep interface androidx.** { *; }

# Keep support library
-keep class android.support.** { *; }

# Remove logging
-assumenosideeffects class android.util.Log {
    public static *** d(...);
    public static *** v(...);
    public static *** i(...);
}

# Optimize
-optimizationpasses 5
-dontusemixedcaseclassnames
-verbose

# Keep native methods
-keepclasseswithmembernames class * {
    native <methods>;
}

# Keep enums
-keepclassmembers enum * {
    public static **[] values();
    public static ** valueOf(java.lang.String);
}
