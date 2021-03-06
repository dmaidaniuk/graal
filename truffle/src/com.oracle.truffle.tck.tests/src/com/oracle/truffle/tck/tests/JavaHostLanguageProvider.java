/*
 * Copyright (c) 2017, 2018, Oracle and/or its affiliates. All rights reserved.
 * DO NOT ALTER OR REMOVE COPYRIGHT NOTICES OR THIS FILE HEADER.
 *
 * The Universal Permissive License (UPL), Version 1.0
 *
 * Subject to the condition set forth below, permission is hereby granted to any
 * person obtaining a copy of this software, associated documentation and/or
 * data (collectively the "Software"), free of charge and under any and all
 * copyright rights in the Software, and any and all patent rights owned or
 * freely licensable by each licensor hereunder covering either (i) the
 * unmodified Software as contributed to or provided by such licensor, or (ii)
 * the Larger Works (as defined below), to deal in both
 *
 * (a) the Software, and
 *
 * (b) any piece of software and/or hardware listed in the lrgrwrks.txt file if
 * one is included with the Software each a "Larger Work" to which the Software
 * is contributed by such licensors),
 *
 * without restriction, including without limitation the rights to copy, create
 * derivative works of, display, perform, and distribute the Software and make,
 * use, sell, offer for sale, import, export, have made, and have sold the
 * Software and the Larger Work(s), and to sublicense the foregoing rights on
 * either these or other terms.
 *
 * This license is subject to the following condition:
 *
 * The above copyright notice and either this complete permission notice or at a
 * minimum a reference to the UPL must be included in all copies or substantial
 * portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 */
package com.oracle.truffle.tck.tests;

import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.function.Consumer;
import java.util.function.Supplier;

import org.graalvm.polyglot.Context;
import org.graalvm.polyglot.Source;
import org.graalvm.polyglot.Value;
import org.graalvm.polyglot.proxy.ProxyArray;
import org.graalvm.polyglot.proxy.ProxyExecutable;
import org.graalvm.polyglot.proxy.ProxyObject;
import org.graalvm.polyglot.tck.LanguageProvider;
import org.graalvm.polyglot.tck.Snippet;
import org.graalvm.polyglot.tck.TypeDescriptor;

public final class JavaHostLanguageProvider implements LanguageProvider {
    private static final String ID = "java-host";

    public JavaHostLanguageProvider() {
    }

    @Override
    public String getId() {
        return ID;
    }

    @Override
    public Collection<? extends Snippet> createValueConstructors(final Context context) {
        final List<Snippet> result = new ArrayList<>();
        final Map<Class<?>, Primitive> primitives = new HashMap<>();
        primitives.put(Boolean.class, Primitive.create("boolean", false, TypeDescriptor.BOOLEAN));
        primitives.put(Byte.class, Primitive.create("byte", Byte.MIN_VALUE, TypeDescriptor.NUMBER));
        primitives.put(Short.class, Primitive.create("short", Short.MIN_VALUE, TypeDescriptor.NUMBER));
        primitives.put(Character.class, Primitive.create("char", ' ', TypeDescriptor.STRING));
        primitives.put(Integer.class, Primitive.create("int", Integer.MIN_VALUE, TypeDescriptor.NUMBER));
        primitives.put(Long.class, Primitive.create("long", Long.MIN_VALUE, TypeDescriptor.NUMBER));
        primitives.put(Float.class, Primitive.create("float", Float.MAX_VALUE, TypeDescriptor.NUMBER));
        primitives.put(Double.class, Primitive.create("double", Double.MAX_VALUE, TypeDescriptor.NUMBER));
        primitives.put(String.class, Primitive.create("java.lang.String", "TEST", TypeDescriptor.STRING));

        // Java primitives
        for (Primitive primitive : primitives.values()) {
            result.add(createPrimitive(context, primitive));
        }
        // Arrays
        result.add(Snippet.newBuilder("Array<int>", export(context, new ValueSupplier<>(new int[]{1, 2})),
                        TypeDescriptor.array(TypeDescriptor.NUMBER)).build());
        result.add(Snippet.newBuilder("Array<java.lang.Object>", export(context, new ValueSupplier<>(new Object[]{1, "TEST"})),
                        TypeDescriptor.array(TypeDescriptor.union(TypeDescriptor.NUMBER, TypeDescriptor.STRING))).build());
        // Primitive Proxies
        for (Primitive primitive : primitives.values()) {
            result.add(createProxyPrimitive(context, primitive));
        }
        // Array Proxies
        result.add(createProxyArray(context, null));
        for (Primitive primitive : primitives.values()) {
            result.add(createProxyArray(context, primitive));
        }
        // Object Proxies
        result.add(Snippet.newBuilder("Proxy<java.lang.Object{}>", export(context, new ValueSupplier<>(ProxyObject.fromMap(Collections.emptyMap()))), TypeDescriptor.OBJECT).build());
        final Map<String, Object> props = new HashMap<>();
        props.put("name", "test");
        result.add(Snippet.newBuilder("Proxy<java.lang.Object{name}>", export(context, new ValueSupplier<>(ProxyObject.fromMap(props))), TypeDescriptor.OBJECT).build());
        // Executable Proxies
        // Generic executable
        result.add(Snippet.newBuilder(
                        "ProxyExecutable<...>",
                        export(context, new ValueSupplier<>(new ProxyExecutableImpl())),
                        TypeDescriptor.EXECUTABLE).build());
        // No-args execuable
        result.add(Snippet.newBuilder(
                        "ProxyExecutable<>",
                        export(context, new ValueSupplier<>(new ProxyExecutableImpl(ProxyExecutableImpl.EMPTY, 0))),
                        TypeDescriptor.executable(TypeDescriptor.ANY)).build());
        for (Primitive primitive : new Primitive[]{
                        primitives.get(Boolean.class),
                        primitives.get(Integer.class),
                        primitives.get(String.class)}) {
            result.add(createProxyExecutable(context, primitive));
        }
        return Collections.unmodifiableCollection(result);
    }

    @Override
    public Value createIdentityFunction(final Context context) {
        return context.asValue(new ProxyExecutable() {
            public Object execute(Value... arguments) {
                return arguments[0];
            }
        });
    }

    @Override
    public Collection<? extends Snippet> createExpressions(final Context context) {
        return Collections.emptyList();
    }

    @Override
    public Collection<? extends Snippet> createStatements(final Context context) {
        return Collections.emptyList();
    }

    @Override
    public Collection<? extends Snippet> createScripts(final Context context) {
        return Collections.emptySet();
    }

    @Override
    public Collection<? extends Source> createInvalidSyntaxScripts(final Context context) {
        return Collections.emptySet();
    }

    private static Snippet createPrimitive(
                    final Context context,
                    final Primitive primitive) {
        return Snippet.newBuilder(
                        primitive.name,
                        export(context,
                                        new ValueSupplier<>(primitive.value)),
                        primitive.type).build();
    }

    private static Snippet createProxyPrimitive(
                    final Context context,
                    final Primitive primitive) {
        return Snippet.newBuilder(
                        String.format("Proxy<%s>", primitive.name),
                        export(context, new ValueSupplier<>(new ProxyPrimitiveImpl(primitive.value))),
                        primitive.type).build();
    }

    private static Snippet createProxyArray(
                    final Context context,
                    final Primitive primitive) {
        return Snippet.newBuilder(
                        String.format("Proxy<Array<%s>>", primitive == null ? "" : primitive.name),
                        export(context, new ValueSupplier<>(primitive == null ? ProxyArray.fromArray() : ProxyArray.fromArray(primitive.value, primitive.value))),
                        primitive == null
                                        ? TypeDescriptor.array(TypeDescriptor.intersection(TypeDescriptor.ARRAY, TypeDescriptor.BOOLEAN, TypeDescriptor.EXECUTABLE, TypeDescriptor.HOST_OBJECT,
                                                        TypeDescriptor.NATIVE_POINTER, TypeDescriptor.NULL, TypeDescriptor.NUMBER, TypeDescriptor.OBJECT, TypeDescriptor.STRING))
                                        : TypeDescriptor.array(primitive.type)).build();
    }

    private static Snippet createProxyExecutable(
                    final Context context,
                    final Primitive primitive) {
        return Snippet.newBuilder(
                        String.format("ProxyExecutable<%s,%s>", primitive.name, primitive.name),
                        export(context, new ValueSupplier<>(new ProxyExecutableImpl(primitive, 2))),
                        TypeDescriptor.executable(primitive.type, primitive.type, primitive.type)).build();
    }

    private static Value export(final Context context, final Supplier<Object> s) {
        return context.asValue(s);
    }

    @SuppressWarnings("deprecation")
    private static final class ProxyPrimitiveImpl implements org.graalvm.polyglot.proxy.ProxyPrimitive {
        private final Object primitiveValue;

        ProxyPrimitiveImpl(final Object primitiveValue) {
            Objects.requireNonNull(primitiveValue);
            this.primitiveValue = primitiveValue;
        }

        @Override
        public Object asPrimitive() {
            return primitiveValue;
        }
    }

    private static final class ValueSupplier<T> implements Supplier<T> {
        private final T value;

        ValueSupplier(T value) {
            this.value = value;
        }

        @Override
        public T get() {
            return value;
        }
    }

    private static final class Primitive {
        final String name;
        final Object value;
        final TypeDescriptor type;

        private Primitive(final String name, final Object value, final TypeDescriptor type) {
            this.name = name;
            this.value = value;
            this.type = type;
        }

        static Primitive create(final String name, final Object value, final TypeDescriptor type) {
            return new Primitive(name, value, type);
        }
    }

    private static final class ProxyExecutableImpl implements ProxyExecutable {
        private static final Consumer<? super Value> EMPTY = new Consumer<Value>() {
            @Override
            public void accept(Value t) {
            }
        };
        private Consumer<? super Value> verifier;
        private final int arity;

        /**
         * Generic executable.
         */
        ProxyExecutableImpl() {
            this(EMPTY, -1);
        }

        /**
         * Executable with concrete parameter types.
         *
         * @param expectedType the expected primitive type
         * @param arity number of required parameters of expectedType
         */
        ProxyExecutableImpl(
                        final Primitive primitive,
                        final int arity) {
            this(createVerifier(primitive), arity);
        }

        ProxyExecutableImpl(
                        final Consumer<? super Value> verifier,
                        final int arity) {
            Objects.requireNonNull(verifier);
            this.verifier = verifier;
            this.arity = arity;
        }

        @Override
        public Object execute(Value... arguments) {
            if (this.arity > arguments.length) {
                throw new AssertionError(String.format("Not enought arguments, required: %d, given: %d", this.arity, arguments.length));
            }
            for (int i = 0; i < arity; i++) {
                verifier.accept(arguments[i]);
            }
            return null;
        }

        private static Consumer<? super Value> createVerifier(final Primitive primitive) {
            if (TypeDescriptor.NUMBER == primitive.type) {
                return new Consumer<Value>() {
                    @Override
                    public void accept(Value value) {
                        if (!value.isNumber()) {
                            throw new AssertionError(String.format("Expected NUMBER, got: %s", value));
                        }
                        if (value.fitsInByte()) {
                            value.asByte();
                        }
                        if (value.fitsInInt()) {
                            value.asInt();
                        }
                        if (value.fitsInLong()) {
                            value.asLong();
                        }
                        if (value.fitsInFloat()) {
                            value.asFloat();
                        }
                        if (value.fitsInDouble()) {
                            value.asDouble();
                        }
                    }
                };
            } else if (TypeDescriptor.BOOLEAN == primitive.type) {
                return new Consumer<Value>() {
                    @Override
                    public void accept(Value value) {
                        value.asBoolean();
                    }
                };
            } else if (TypeDescriptor.STRING == primitive.type) {
                return new Consumer<Value>() {
                    @Override
                    public void accept(Value value) {
                        value.asString();
                    }
                };
            } else {
                return EMPTY;
            }
        }
    }
}
