# React Hook Form

## Definition
React Hook Form is a performance-first form library for React that provides performant, flexible, and extensible forms with easy-to-use validation. It uses uncontrolled components and native HTML validation to minimize re-renders.

## Why Do We Need It?
- **Performance**: Minimal re-renders using uncontrolled components
- **Developer Experience**: Simple, intuitive API
- **Validation**: Flexible validation with built-in or external libraries
- **TypeScript**: Excellent TypeScript support
- **Bundle Size**: Tiny bundle with zero dependencies

## How It Works

```
┌─────────────────────────────────────────────────────────────────────┐
│                    REACT HOOK FORM ARCHITECTURE                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    useForm Hook                               │   │
│  │  • register: Register input fields                           │   │
│  │  • handleSubmit: Handle form submission                      │   │
│  │  • formState: Form state and validation                      │   │
│  │  • control: Controller for controlled components             │   │
│  │  • watch: Watch field values                                 │   │
│  │  • reset: Reset form state                                   │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                      │
│                              ▼                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                  Uncontrolled Inputs                          │   │
│  │  • Uses native HTML input validation                         │   │
│  │  • No controlled state per field                             │   │
│  │  • Ref-based access to input values                         │   │
│  │  • Minimal re-renders                                        │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                      │
│                              ▼                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                  Validation Layer                            │   │
│  │  • Built-in HTML5 validation                                │   │
│  │  • Schema validation (Zod, Yup, Joi)                        │   │
│  │  • Custom validation functions                               │   │
│  │  • Field-level and form-level validation                     │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## Code Examples

### 1. Basic Form with useForm

```typescript
import { useForm } from 'react-hook-form';

interface LoginForm {
  email: string;
  password: string;
}

function LoginPage() {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<LoginForm>({
    defaultValues: {
      email: '',
      password: '',
    },
  });

  const onSubmit = async (data: LoginForm) => {
    // API call
    console.log(data);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <div>
        <label htmlFor="email">Email</label>
        <input
          id="email"
          type="email"
          {...register('email', {
            required: 'Email is required',
            pattern: {
              value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
              message: 'Invalid email address',
            },
          })}
        />
        {errors.email && <span>{errors.email.message}</span>}
      </div>

      <div>
        <label htmlFor="password">Password</label>
        <input
          id="password"
          type="password"
          {...register('password', {
            required: 'Password is required',
            minLength: {
              value: 8,
              message: 'Password must be at least 8 characters',
            },
          })}
        />
        {errors.password && <span>{errors.password.message}</span>}
      </div>

      <button type="submit" disabled={isSubmitting}>
        {isSubmitting ? 'Logging in...' : 'Login'}
      </button>
    </form>
  );
}
```

### 2. Form with Zod Validation

```typescript
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

const registerSchema = z.object({
  username: z.string().min(3, 'Username must be at least 3 characters'),
  email: z.string().email('Invalid email address'),
  password: z
    .string()
    .min(8, 'Password must be at least 8 characters')
    .regex(/[A-Z]/, 'Password must contain at least one uppercase letter')
    .regex(/[0-9]/, 'Password must contain at least one number'),
  confirmPassword: z.string(),
}).refine((data) => data.password === data.confirmPassword, {
  message: 'Passwords do not match',
  path: ['confirmPassword'],
});

type RegisterFormData = z.infer<typeof registerSchema>;

function RegisterForm() {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<RegisterFormData>({
    resolver: zodResolver(registerSchema),
  });

  const onSubmit = async (data: RegisterFormData) => {
    // API call
    console.log(data);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <div>
        <label htmlFor="username">Username</label>
        <input id="username" {...register('username')} />
        {errors.username && <span>{errors.username.message}</span>}
      </div>

      <div>
        <label htmlFor="email">Email</label>
        <input id="email" type="email" {...register('email')} />
        {errors.email && <span>{errors.email.message}</span>}
      </div>

      <div>
        <label htmlFor="password">Password</label>
        <input id="password" type="password" {...register('password')} />
        {errors.password && <span>{errors.password.message}</span>}
      </div>

      <div>
        <label htmlFor="confirmPassword">Confirm Password</label>
        <input
          id="confirmPassword"
          type="password"
          {...register('confirmPassword')}
        />
        {errors.confirmPassword && (
          <span>{errors.confirmPassword.message}</span>
        )}
      </div>

      <button type="submit">Register</button>
    </form>
  );
}
```

### 3. Form with Controller (Controlled Components)

```typescript
import { useForm, Controller } from 'react-hook-form';
import Select from 'react-select';
import DatePicker from 'react-datepicker';

interface EventForm {
  name: string;
  category: string;
  date: Date | null;
  description: string;
}

function EventForm() {
  const {
    register,
    handleSubmit,
    control,
    formState: { errors },
  } = useForm<EventForm>({
    defaultValues: {
      name: '',
      category: '',
      date: null,
      description: '',
    },
  });

  const onSubmit = async (data: EventForm) => {
    console.log(data);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <div>
        <label htmlFor="name">Event Name</label>
        <input id="name" {...register('name', { required: true })} />
        {errors.name && <span>This field is required</span>}
      </div>

      <div>
        <label>Category</label>
        <Controller
          name="category"
          control={control}
          rules={{ required: true }}
          render={({ field }) => (
            <Select
              {...field}
              options={[
                { value: 'conference', label: 'Conference' },
                { value: 'meetup', label: 'Meetup' },
                { value: 'workshop', label: 'Workshop' },
              ]}
            />
          )}
        />
        {errors.category && <span>This field is required</span>}
      </div>

      <div>
        <label>Date</label>
        <Controller
          name="date"
          control={control}
          render={({ field }) => (
            <DatePicker
              {...field}
              selected={field.value}
              onChange={(date) => field.onChange(date)}
            />
          )}
        />
      </div>

      <div>
        <label htmlFor="description">Description</label>
        <textarea id="description" {...register('description')} />
      </div>

      <button type="submit">Create Event</button>
    </form>
  );
}
```

### 4. Form with Watch and Dynamic Fields

```typescript
import { useForm, useFieldArray } from 'react-hook-form';

interface OrderForm {
  customerName: string;
  items: {
    name: string;
    quantity: number;
    price: number;
  }[];
}

function OrderForm() {
  const {
    register,
    handleSubmit,
    control,
    watch,
    formState: { errors },
  } = useForm<OrderForm>({
    defaultValues: {
      customerName: '',
      items: [{ name: '', quantity: 1, price: 0 }],
    },
  });

  const { fields, append, remove } = useFieldArray({
    control,
    name: 'items',
  });

  // Watch all items to calculate total
  const items = watch('items');
  const total = items.reduce(
    (sum, item) => sum + item.quantity * item.price,
    0
  );

  const onSubmit = async (data: OrderForm) => {
    console.log(data);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <div>
        <label htmlFor="customerName">Customer Name</label>
        <input id="customerName" {...register('customerName', { required: true })} />
        {errors.customerName && <span>This field is required</span>}
      </div>

      <div>
        <h3>Items</h3>
        {fields.map((field, index) => (
          <div key={field.id}>
            <input
              {...register(`items.${index}.name`, { required: true })}
              placeholder="Item name"
            />
            <input
              type="number"
              {...register(`items.${index}.quantity`, { required: true, min: 1 })}
              placeholder="Quantity"
            />
            <input
              type="number"
              {...register(`items.${index}.price`, { required: true, min: 0 })}
              placeholder="Price"
            />
            <button type="button" onClick={() => remove(index)}>
              Remove
            </button>
          </div>
        ))}
        <button type="button" onClick={() => append({ name: '', quantity: 1, price: 0 })}>
          Add Item
        </button>
      </div>

      <div>
        <strong>Total: ${total.toFixed(2)}</strong>
      </div>

      <button type="submit">Place Order</button>
    </form>
  );
}
```

### 5. Form with Async Validation

```typescript
import { useForm } from 'react-hook-form';

interface UsernameForm {
  username: string;
}

function UsernameForm() {
  const {
    register,
    handleSubmit,
    formState: { errors, isValidating },
  } = useForm<UsernameForm>({
    mode: 'onChange',
  });

  const validateUsername = async (username: string) => {
    // Simulate API call to check username availability
    const response = await fetch(`/api/check-username?username=${username}`);
    const data = await response.json();

    if (data.exists) {
      return 'Username is already taken';
    }
    return true;
  };

  const onSubmit = async (data: UsernameForm) => {
    console.log(data);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <div>
        <label htmlFor="username">Username</label>
        <input
          id="username"
          {...register('username', {
            required: 'Username is required',
            minLength: {
              value: 3,
              message: 'Username must be at least 3 characters',
            },
            validate: validateUsername,
          })}
        />
        {isValidating && <span>Checking availability...</span>}
        {errors.username && <span>{errors.username.message}</span>}
      </div>

      <button type="submit">Check Username</button>
    </form>
  );
}
```

## Real-World Use Cases

### Multi-Step Form
```typescript
import { useForm, FormProvider } from 'react-hook-form';

function MultiStepForm() {
  const methods = useForm({
    mode: 'onChange',
  });

  const [step, setStep] = useState(1);

  const onSubmit = async (data: any) => {
    if (step < 3) {
      setStep(step + 1);
    } else {
      // Submit final data
      console.log(data);
    }
  };

  return (
    <FormProvider {...methods}>
      <form onSubmit={methods.handleSubmit(onSubmit)}>
        {step === 1 && <Step1 />}
        {step === 2 && <Step2 />}
        {step === 3 && <Step3 />}

        <div>
          {step > 1 && (
            <button type="button" onClick={() => setStep(step - 1)}>
              Previous
            </button>
          )}
          <button type="submit">
            {step === 3 ? 'Submit' : 'Next'}
          </button>
        </div>
      </form>
    </FormProvider>
  );
}
```

## Common Mistakes

1. **Using Controller unnecessarily**: Use `register` for native inputs
2. **Not using mode**: Missing validation triggers
3. **Over-watching**: Watching entire form when only specific fields needed
4. **Missing default values**: Not providing initial values
5. **Not handling async validation properly**: Missing loading states

## Best Practices

1. **Use `register` for native inputs**: Avoid Controller for simple inputs
2. **Use Zod/Yup for complex validation**: Schema validation is cleaner
3. **Use `mode: 'onChange'` for real-time validation**: Better UX
4. **Use `useFieldArray` for dynamic lists**: Built-in support
5. **Use FormProvider for complex forms**: Share form context

## Performance Considerations

```
React Hook Form Performance:
┌─────────────────────────────────────────────────────────────────┐
│  Uncontrolled Components:                                        │
│  • No re-render on each keystroke                               │
│  • Ref-based value access                                       │
│  • Native HTML validation                                       │
│                                                                 │
│  Optimized Re-renders:                                           │
│  • Only affected components re-render                           │
│  • FormState is optimized                                      │
│  • Minimal context updates                                      │
│                                                                 │
│  Bundle Size:                                                    │
│  • ~9KB gzipped                                                 │
│  • Zero dependencies                                            │
│  • Tree-shakeable                                               │
└─────────────────────────────────────────────────────────────────┘
```

## Interview Questions

### Beginner (5)
1. **What is React Hook Form?**
   - Answer: A performance-first form library for React that uses uncontrolled components and native HTML validation to minimize re-renders.

2. **What is the `register` function?**
   - Answer: A function that registers input fields with React Hook Form, providing validation and state management.

3. **What is `handleSubmit`?**
   - Answer: A function that handles form submission, validates all fields, and calls the submit handler with form data.

4. **What is `formState`?**
   - Answer: An object containing form state like errors, isSubmitting, isDirty, isValid, etc.

5. **What is `Controller`?**
   - Answer: A component for integrating controlled third-party components with React Hook Form.

### Intermediate (5)
6. **What is the difference between `register` and `Controller`?**
   - Answer: `register` is for native HTML inputs (uncontrolled); `Controller` is for third-party components that need controlled state.

7. **How do you handle dynamic fields?**
   - Answer: Use `useFieldArray` hook to manage dynamic lists of fields with add, remove, and move operations.

8. **What is the `watch` function?**
   - Answer: A function that watches specific fields and re-renders when their values change.

9. **How do you handle async validation?**
   - Answer: Return a promise from validation function; React Hook Form handles loading state and validation.

10. **What is the `mode` option?**
    - Answer: Determines when validation runs (onSubmit, onChange, onBlur, all).

### Senior (10)
11. **How does React Hook Form achieve better performance?**
    - Answer: Uses uncontrolled components, ref-based access, minimal re-renders, and optimized state management.

12. **How do you integrate with Zod?**
    - Answer: Use `zodResolver` from `@hookform/resolvers/zod` as the resolver option in `useForm`.

13. **How do you handle complex nested objects?**
    - Answer: Use dot notation in register (e.g., `register('user.address.city')`) or nested field arrays.

14. **How do you handle form-level validation?**
    - Answer: Use `validate` option in `useForm` or custom validation logic in submit handler.

15. **How do you optimize re-renders?**
    - Answer: Use `watch` with selector, avoid unnecessary Controller usage, use `useFormContext` appropriately.

16. **How do you handle server-side validation errors?**
    - Answer: Use `setError` to set errors from server response, or `setError('root.serverError')` for form-level errors.

17. **How do you handle file uploads?**
    - Answer: Use `register` with `valueAs` option or Controller with controlled component.

18. **How do you handle multi-step forms?**
    - Answer: Use `FormProvider` to share form context, or maintain separate forms per step.

19. **How do you test React Hook Form components?**
    - Answer: Use `renderHook` with `useForm`, or test form components with `@testing-library/react`.

20. **How do you handle conditional fields?**
    - Answer: Use `watch` to conditionally render fields and apply conditional validation.

### FAANG-style (5)
21. **Design a form system for a large application**
- **Answer**:
  - React Hook Form for performance
  - Zod for schema validation
  - FormProvider for context
  - Custom hooks for common patterns
  - Storybook for documentation

22. **How would you handle forms in a micro-frontend architecture?**
- **Answer**:
  - Independent form libraries per micro-frontend
  - Shared validation schemas
  - Event-based communication
  - Consistent UX patterns

23. **Explain form validation architecture**
- **Answer**:
  - Client-side: Zod schemas
  - Server-side: Same schemas with additional rules
  - Real-time validation with debouncing
  - Accessibility considerations

24. **How do you optimize form performance at scale?**
- **Answer**:
  - Memoization of validation functions
  - Debounced validation
  - Lazy loading of complex fields
  - Virtualization for long lists

25. **Design a form builder system**
- **Answer**:
  - JSON schema for form definition
  - Dynamic component rendering
  - Validation rule engine
  - Accessibility compliance
  - Performance optimization

### Follow-ups (5)
26. **How do you handle forms in server-side rendering?**
- **Answer**: Use `defaultValues` with `useEffect`, or hydrate form state from server.

27. **How do you handle offline form submission?**
- **Answer**: Store form data in localStorage/IndexedDB, sync when online.

28. **How do you handle form analytics?**
- **Answer**: Track field interactions, submission attempts, validation errors, and completion rates.

29. **How do you handle form accessibility?**
- **Answer**: Use proper labels, ARIA attributes, error announcements, and keyboard navigation.

30. **How do you handle form internationalization?**
- **Answer**: Use i18n libraries for labels and error messages, support RTL layouts.

## Summary

React Hook Form provides a performant, developer-friendly approach to form management in React. Master its API, validation integration, and best practices for building excellent forms.

## References & Learn More

- [React Hook Form Documentation](https://react-hook-form.com/)
- [React Hook Form GitHub](https://github.com/react-hook-form/react-hook-form)
- [Zod Integration](https://react-hook-form.com/docs/useform/resolver#zod)
- [useFieldArray](https://react-hook-form.com/docs/usefieldarray)
- [Controller](https://react-hook-form.com/docs/usecontroller)
