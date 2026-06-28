# Formik

## Definition
Formik is a popular React form library that helps with form state management, validation, and submission. It provides a set of components and hooks for building forms with React, focusing on simplicity and developer experience.

## Why Do We Need It?
- **Form State Management**: Handles form state automatically
- **Validation**: Built-in validation with Yup integration
- **Error Handling**: Automatic error state management
- **Submission**: Handles form submission and errors
- **Performance**: Optimized for React with shouldComponentUpdate

## How It Works

```
┌─────────────────────────────────────────────────────────────────────┐
│                        FORMIK ARCHITECTURE                           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    Formik Component/ Hook                     │   │
│  │  • values: Form values                                       │   │
│  │  • errors: Validation errors                                 │   │
│  │  • touched: Touched fields                                   │   │
│  │  • handleChange: Field change handler                        │   │
│  │  • handleBlur: Field blur handler                            │   │
│  │  • handleSubmit: Form submission handler                     │   │
│  │  • isSubmitting: Submission state                            │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                      │
│                              ▼                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                  Controlled Components                        │   │
│  │  • Formikik: Form wrapper                                    │   │
│  │  • Field: Input wrapper                                      │   │
│  │  • ErrorMessage: Error display                               │   │
│  │  • Form: Form element                                        │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                      │
│                              ▼                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                  Validation Layer                            │   │
│  │  • Yup schema (default)                                     │   │
│  │  • Custom validation functions                               │   │
│  │  • Field-level and form-level validation                     │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## Code Examples

### 1. Basic Formik Usage

```typescript
import { Formik, Form, Field, ErrorMessage } from 'formik';
import * as Yup from 'yup';

const loginSchema = Yup.object().shape({
  email: Yup.string()
    .email('Invalid email address')
    .required('Email is required'),
  password: Yup.string()
    .min(8, 'Password must be at least 8 characters')
    .required('Password is required'),
});

function LoginForm() {
  return (
    <Formik
      initialValues={{ email: '', password: '' }}
      validationSchema={loginSchema}
      onSubmit={(values, { setSubmitting }) => {
        setTimeout(() => {
          console.log(values);
          setSubmitting(false);
        }, 400);
      }}
    >
      {({ isSubmitting }) => (
        <Form>
          <div>
            <label htmlFor="email">Email</label>
            <Field id="email" name="email" type="email" />
            <ErrorMessage name="email" component="div" className="error" />
          </div>

          <div>
            <label htmlFor="password">Password</label>
            <Field id="password" name="password" type="password" />
            <ErrorMessage name="password" component="div" className="error" />
          </div>

          <button type="submit" disabled={isSubmitting}>
            {isSubmitting ? 'Logging in...' : 'Login'}
          </button>
        </Form>
      )}
    </Formik>
  );
}
```

### 2. Formik with useFormik Hook

```typescript
import { useFormik } from 'formik';
import * as Yup from 'yup';

const registerSchema = Yup.object().shape({
  username: Yup.string()
    .min(3, 'Username must be at least 3 characters')
    .required('Username is required'),
  email: Yup.string()
    .email('Invalid email address')
    .required('Email is required'),
  password: Yup.string()
    .min(8, 'Password must be at least 8 characters')
    .required('Password is required'),
  confirmPassword: Yup.string()
    .oneOf([Yup.ref('password')], 'Passwords must match')
    .required('Please confirm your password'),
});

function RegisterForm() {
  const formik = useFormik({
    initialValues: {
      username: '',
      email: '',
      password: '',
      confirmPassword: '',
    },
    validationSchema: registerSchema,
    onSubmit: (values) => {
      console.log(values);
    },
  });

  return (
    <form onSubmit={formik.handleSubmit}>
      <div>
        <label htmlFor="username">Username</label>
        <input
          id="username"
          name="username"
          type="text"
          onChange={formik.handleChange}
          onBlur={formik.handleBlur}
          value={formik.values.username}
        />
        {formik.touched.username && formik.errors.username && (
          <div className="error">{formik.errors.username}</div>
        )}
      </div>

      <div>
        <label htmlFor="email">Email</label>
        <input
          id="email"
          name="email"
          type="email"
          onChange={formik.handleChange}
          onBlur={formik.handleBlur}
          value={formik.values.email}
        />
        {formik.touched.email && formik.errors.email && (
          <div className="error">{formik.errors.email}</div>
        )}
      </div>

      <div>
        <label htmlFor="password">Password</label>
        <input
          id="password"
          name="password"
          type="password"
          onChange={formik.handleChange}
          onBlur={formik.handleBlur}
          value={formik.values.password}
        />
        {formik.touched.password && formik.errors.password && (
          <div className="error">{formik.errors.password}</div>
        )}
      </div>

      <div>
        <label htmlFor="confirmPassword">Confirm Password</label>
        <input
          id="confirmPassword"
          name="confirmPassword"
          type="password"
          onChange={formik.handleChange}
          onBlur={formik.handleBlur}
          value={formik.values.confirmPassword}
        />
        {formik.touched.confirmPassword && formik.errors.confirmPassword && (
          <div className="error">{formikik.errors.confirmPassword}</div>
        )}
      </div>

      <button type="submit" disabled={formik.isSubmitting}>
        Register
      </button>
    </form>
  );
}
```

### 3. Custom Field Component

```typescript
import { useField, FieldProps } from 'formik';

interface CustomInputProps extends FieldProps {
  label: string;
  type?: string;
  placeholder?: string;
}

function CustomInput({ label, type = 'text', placeholder, ...props }: CustomInputProps) {
  const [field, meta] = useField(props);

  return (
    <div className="form-group">
      <label htmlFor={field.name}>{label}</label>
      <input
        {...field}
        id={field.name}
        type={type}
        placeholder={placeholder}
        className={meta.touched && meta.error ? 'input-error' : ''}
      />
      {meta.touched && meta.error && (
        <div className="error">{meta.error}</div>
      )}
    </div>
  );
}

// Usage
function ContactForm() {
  return (
    <Formik
      initialValues={{ name: '', email: '', message: '' }}
      onSubmit={(values) => console.log(values)}
    >
      <Form>
        <CustomInput label="Name" name="name" />
        <CustomInput label="Email" name="email" type="email" />
        <CustomInput label="Message" name="message" />
        <button type="submit">Send</button>
      </Form>
    </Formik>
  );
}
```

### 4. Dynamic Fields with FieldArray

```typescript
import { Formik, Form, Field, FieldArray, ErrorMessage } from 'formik';

interface OrderItem {
  name: string;
  quantity: number;
  price: number;
}

interface OrderFormValues {
  customerName: string;
  items: OrderItem[];
}

const initialValues: OrderFormValues = {
  customerName: '',
  items: [{ name: '', quantity: 1, price: 0 }],
};

function OrderForm() {
  return (
    <Formik
      initialValues={initialValues}
      onSubmit={(values) => console.log(values)}
    >
      {({ values }) => (
        <Form>
          <div>
            <label htmlFor="customerName">Customer Name</label>
            <Field id="customerName" name="customerName" />
          </div>

          <FieldArray name="items">
            {({ push, remove }) => (
              <div>
                <h3>Items</h3>
                {values.items.map((item, index) => (
                  <div key={index} className="item-row">
                    <Field name={`items.${index}.name`} placeholder="Item name" />
                    <Field
                      name={`items.${index}.quantity`}
                      type="number"
                      placeholder="Quantity"
                    />
                    <Field
                      name={`items.${index}.price`}
                      type="number"
                      placeholder="Price"
                    />
                    <button type="button" onClick={() => remove(index)}>
                      Remove
                    </button>
                  </div>
                ))}
                <button
                  type="button"
                  onClick={() => push({ name: '', quantity: 1, price: 0 })}
                >
                  Add Item
                </button>
              </div>
            )}
          </FieldArray>

          <div>
            <strong>
              Total: $
              {values.items
                .reduce((sum, item) => sum + item.quantity * item.price, 0)
                .toFixed(2)}
            </strong>
          </div>

          <button type="submit">Place Order</button>
        </Form>
      )}
    </Formik>
  );
}
```

### 5. Custom Validation

```typescript
import { Formik, Form, Field, ErrorMessage } from 'formik';

interface FormValues {
  email: string;
  password: string;
}

function validateEmail(value: string) {
  let error;
  if (!value) {
    error = 'Email is required';
  } else if (!/^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i.test(value)) {
    error = 'Invalid email address';
  }
  return error;
}

function validatePassword(value: string) {
  let error;
  if (!value) {
    error = 'Password is required';
  } else if (value.length < 8) {
    error = 'Password must be at least 8 characters';
  } else if (!/[A-Z]/.test(value)) {
    error = 'Password must contain at least one uppercase letter';
  } else if (!/[0-9]/.test(value)) {
    error = 'Password must contain at least one number';
  }
  return error;
}

function LoginForm() {
  return (
    <Formik
      initialValues={{ email: '', password: '' }}
      onSubmit={(values) => console.log(values)}
    >
      <Form>
        <div>
          <label htmlFor="email">Email</label>
          <Field
            id="email"
            name="email"
            type="email"
            validate={validateEmail}
          />
          <ErrorMessage name="email" component="div" className="error" />
        </div>

        <div>
          <label htmlFor="password">Password</label>
          <Field
            id="password"
            name="password"
            type="password"
            validate={validatePassword}
          />
          <ErrorMessage name="password" component="div" className="error" />
        </div>

        <button type="submit">Login</button>
      </Form>
    </Formik>
  );
}
```

### 6. Formik with TypeScript

```typescript
import { Formik, Form, Field, FormikProps } from 'formik';
import * as Yup from 'yup';

interface ContactFormValues {
  name: string;
  email: string;
  subject: string;
  message: string;
}

const validationSchema = Yup.object().shape({
  name: Yup.string().required('Name is required'),
  email: Yup.string().email('Invalid email').required('Email is required'),
  subject: Yup.string().required('Subject is required'),
  message: Yup.string().required('Message is required'),
});

function ContactForm() {
  const initialValues: ContactFormValues = {
    name: '',
    email: '',
    subject: '',
    message: '',
  };

  const handleSubmit = (values: ContactFormValues) => {
    console.log(values);
  };

  return (
    <Formik
      initialValues={initialValues}
      validationSchema={validationSchema}
      onSubmit={handleSubmit}
    >
      {(props: FormikProps<ContactFormValues>) => (
        <Form>
          <Field name="name" placeholder="Name" />
          {props.touched.name && props.errors.name && (
            <div>{props.errors.name}</div>
          )}

          <Field name="email" type="email" placeholder="Email" />
          {props.touched.email && props.errors.email && (
            <div>{props.errors.email}</div>
          )}

          <Field name="subject" placeholder="Subject" />
          {props.touched.subject && props.errors.subject && (
            <div>{props.errors.subject}</div>
          )}

          <Field name="message" as="textarea" placeholder="Message" />
          {props.touched.message && props.errors.message && (
            <div>{props.errors.message}</div>
          )}

          <button type="submit" disabled={props.isSubmitting}>
            Send
          </button>
        </Form>
      )}
    </Formik>
  );
}
```

## Real-World Use Cases

### Multi-Step Form
```typescript
import { Formik, Form, Step } from 'formik';

function MultiStepForm() {
  const [step, setStep] = useState(1);

  const step1Validation = Yup.object().shape({
    name: Yup.string().required(),
    email: Yup.string().email().required(),
  });

  const step2Validation = Yup.object().shape({
    address: Yup.string().required(),
    city: Yup.string().required(),
  });

  return (
    <Formik
      initialValues={{ name: '', email: '', address: '', city: '' }}
      onSubmit={(values) => {
        if (step < 3) {
          setStep(step + 1);
        } else {
          console.log(values);
        }
      }}
    >
      {() => (
        <Form>
          {step === 1 && <Step1 />}
          {step === 2 && <Step2 />}
          {step === 3 && <Step3 />}

          <button type="submit">
            {step === 3 ? 'Submit' : 'Next'}
          </button>
        </Form>
      )}
    </Formik>
  );
}
```

## Common Mistakes

1. **Not using touched**: Only showing errors after field interaction
2. **Over-validating**: Validating on every keystroke unnecessarily
3. **Not handling reset**: Forgetting to reset form after submission
4. **Missing loading states**: Not showing submission progress
5. **Poor accessibility**: Missing labels and ARIA attributes

## Best Practices

1. **Use validation schemas**: Define validation rules declaratively
2. **Use Field component**: Leverage Formik's optimized Field component
3. **Handle touched state**: Show errors only after user interaction
4. **Provide loading feedback**: Disable submit button during submission
5. **Use TypeScript**: Define form value interfaces

## Performance Considerations

```
Formik Performance:
┌─────────────────────────────────────────────────────────────────┐
│  Optimizations:                                                  │
│  • shouldComponentUpdate in Formik component                   │
│  • Field-level re-rendering                                    │
│  • Memoized validation                                         │
│  • Optimized context                                           │
│                                                                 │
│  Considerations:                                                │
│  • Controlled components (unlike React Hook Form)              │
│  • More re-renders than uncontrolled approaches                │
│  • Context updates can affect performance                      │
│                                                                 │
│  Best Practices:                                                │
│  • Use Formik component over useFormik for performance         │
│  • Minimize context consumers                                  │
│  • Use custom Field components                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Interview Questions

### Beginner (5)
1. **What is Formik?**
   - Answer: A React form library that handles form state management, validation, and submission.

2. **What is the difference between Formik component and useFormik hook?**
   - Answer: Formik component provides context and render props; useFormik hook is for custom components.

3. **What is the Field component?**
   - Answer: A component that connects input elements to Formik state with automatic onChange and onBlur handlers.

4. **What is Yup?**
   - Answer: A JavaScript schema builder commonly used with Formik for validation.

5. **What is the touched state?**
   - Answer: An object tracking which fields have been focused and blurred.

### Intermediate (5)
6. **How do you handle form submission?**
   - Answer: Use `onSubmit` prop with Formik component or `handleSubmit` from useFormik hook.

7. **How do you reset a form?**
   - Answer: Use `resetForm` method or pass `initialValues` to `resetForm`.

8. **How do you handle async validation?**
   - Answer: Return a Promise from validation function.

9. **How do you access form state in child components?**
   - Answer: Use `useFormikContext` hook or render props pattern.

10. **How do you handle multiple forms?**
    - Answer: Each Formik instance is independent; use separate instances.

### Senior (10)
11. **What is the difference between Formik and React Hook Form?**
    - Answer: Formik uses controlled components; React Hook Form uses uncontrolled components for better performance.

12. **How do you optimize Formik performance?**
    - Answer: Use Formik component, minimize context consumers, use custom Field components.

13. **How do you handle complex validation?**
    - Answer: Use Yup's `when` for conditional validation or custom validation functions.

14. **How do you integrate Formik with Redux?**
    - Answer: Use `mapDispatchToProps` or connect Formik state to Redux store.

15. **How do you handle file uploads?**
    - Answer: Use Field component with type="file" and handle in onChange.

16. **How do you handle form persistence?**
    - Answer: Store form state in localStorage and restore on mount.

17. **How do you handle form analytics?**
    - Answer: Track field interactions using Formik's callbacks.

18. **How do you handle form accessibility?**
    - Answer: Use Field component with labels, aria attributes, and error announcements.

19. **How do you test Formik components?**
    - Answer: Use @testing-library/react with Formik's simulated events.

20. **How do you handle form in server-side rendering?**
    - Answer: Pass initial values from server and hydrate Formik state.

### FAANG-style (5)
21. **Design a form system for a large application**
- **Answer**:
  - Formik for form management
  - Yup for validation
  - Custom Field components
  - Form templates
  - Accessibility compliance

22. **How would you migrate from Formik to React Hook Form?**
- **Answer**:
  - Migrate validation schemas
  - Replace controlled with uncontrolled components
  - Update form submission logic
  - Test thoroughly

23. **Explain Formik's architecture**
- **Answer**:
  - Context-based state management
  - Render props pattern
  - Field-level optimization
  - Yup integration

24. **How do you handle forms in micro-frontends?**
- **Answer**:
  - Independent Formik instances
  - Shared validation schemas
  - Event-based communication

25. **Design a form validation system**
- **Answer**:
  - Yup schemas for validation
  - Custom validation rules
  - Error formatting
  - Accessibility compliance

### Follow-ups (5)
26. **How do you handle Formik in React Server Components?**
- **Answer**: Use initial values from server, hydrate Formik state on client.

27. **How do you handle Formik with GraphQL?**
- **Answer**: Use Apollo Client or react-query for form submissions and validation.

28. **How do you handle Formik in TypeScript?**
- **Answer**: Define form value interfaces, use FormikProps for type safety.

29. **How do you handle Formik form persistence?**
- **Answer**: Use localStorage or sessionStorage to persist form state.

30. **How do you handle Formik with third-party components?**
- **Answer**: Use Field component with custom render props or useField hook.

## Summary

Formik provides a comprehensive solution for form management in React. While it offers excellent developer experience, consider React Hook Form for better performance in large forms.

## References & Learn More

- [Formik Documentation](https://formik.org/)
- [Formik GitHub](https://github.com/jaredpalmer/formik)
- [Yup Documentation](https://github.com/jquense/yup)
- [Formik Examples](https://formik.org/docs/examples)
- [Formik TypeScript Guide](https://formik.org/docs/guides/typescript)
