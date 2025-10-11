export async function GET(request: Request) {
  return Response.json({ message: 'Hello from Next.js API!' })
}



// import { NextResponse } from 'next/server';

// export async function POST(request: Request) {
//   const data = await request.json();
//   console.log("Received data:", data);

//   return NextResponse.json({ message: 'POST request received', data });
// }

// import { NextResponse } from 'next/server';

// export async function PATCH(request: Request) {
//   try {
//     const data = await request.json();

//     // Example: update a user's name
//     const updatedUser = {
//       id: 1,
//       name: data.name || 'Default User',
//       email: 'user@example.com'
//     };

//     return NextResponse.json({
//       message: 'User updated successfully',
//       user: updatedUser
//     });

//   } catch (error) {
//     return NextResponse.json(
//       { error: 'Failed to process PATCH request' },
//       { status: 400 }
//     );
//   }
// }


// delete method in next.js 
import { NextResponse } from 'next/server';

export async function DELETE(request: Request) {
  try {
    // If you're passing an ID in the request body
    const { id } = await request.json();

    // Example: simulate deleting a user
    console.log(`Deleting user with ID: ${id}`);

    return NextResponse.json({
      message: `User with ID ${id} deleted successfully`,
    });
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to delete user' },
      { status: 400 }
    );
  }
}
