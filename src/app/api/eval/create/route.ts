import { createClient } from '@supabase/supabase-js';

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);

export async function POST(req: Request) {
  try {
    const { file_url, rubric_id } = await req.json();

    if (!file_url || !rubric_id) {
      return Response.json({ error: 'Missing required fields' }, { status: 400 });
    }

    const { data, error } = await supabase
      .from('eval_jobs')
      .insert({
        file_url,
        rubric_id,
        status: 'pending',
        created_by: (await supabase.auth.getUser()).data.user?.id || null
      })
      .select()
      .single();

    if (error) throw error;

    return Response.json({ success: true, job: data });
  } catch (err: any) {
    console.error('Error creating job:', err);
    return Response.json({ error: err.message }, { status: 500 });
  }
}
