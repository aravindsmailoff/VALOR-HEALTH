import { NextRequest, NextResponse } from "next/server";

/**
 * Proxy Route Handler to internal AegisTwin FastAPI service.
 * In Vercel Services, process.env.AEGISTWIN_URL is injected via service bindings.
 */
export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ path: string[] }> }
) {
  const { path } = await params;
  return forwardRequest(request, path.join("/"));
}

export async function POST(
  request: NextRequest,
  { params }: { params: Promise<{ path: string[] }> }
) {
  const { path } = await params;
  return forwardRequest(request, path.join("/"));
}

async function forwardRequest(request: NextRequest, subpath: string) {
  // Read Vercel service binding, falling back to local port 8000
  const baseUrl =
    process.env.AEGISTWIN_URL ||
    process.env.NEXT_PUBLIC_API_URL ||
    "http://127.0.0.1:8000";

  const targetUrl = new URL(subpath, baseUrl.endsWith("/") ? baseUrl : `${baseUrl}/`);
  
  // Forward search query params
  targetUrl.search = request.nextUrl.search;

  try {
    const headers = new Headers(request.headers);
    // Remove host header to let fetch set the target host
    headers.delete("host");

    const body =
      request.method !== "GET" && request.method !== "HEAD"
        ? await request.text()
        : undefined;

    const response = await fetch(targetUrl.toString(), {
      method: request.method,
      headers,
      body,
    });

    const data = await response.text();
    return new NextResponse(data, {
      status: response.status,
      headers: {
        "Content-Type": response.headers.get("Content-Type") || "application/json",
      },
    });
  } catch (error: any) {
    return NextResponse.json(
      {
        error: "Failed to connect to AegisTwin service",
        target: targetUrl.toString(),
        details: error?.message,
      },
      { status: 502 }
    );
  }
}
